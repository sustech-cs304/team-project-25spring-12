import os
import glob
import json
import shutil
import hashlib

import requests

import mjc.config as mjc_config
import mjc.utils.judger_config as judger_config

md = hashlib.md5()
judge_result = {
    -1: 'WRONG_ANSWER',
    0: 'ACCEPT',
    1: 'CPU_TIME_LIMIT_EXCEEDED',
    2: 'REAL_TIME_LIMIT_EXCEEDED',
    3: 'MEMORY_LIMIT_EXCEEDED',
    4: 'RUNTIME_ERROR',
    5: 'SYSTEM_ERROR'
}


def build_judge_request(src: str, lang_cfg: dict, test_case_id: str,
                        max_cpu_time: int = 1000, max_memory: int = 134217728):
    request_header = {
        "X-Judge-Server-Token": mjc_config.OJ_TOKEN,
    }
    request_body = {
        "src": src,
        "language_config": lang_cfg,
        "max_cpu_time": max_cpu_time,
        "max_memory": max_memory,
        "test_case_id": test_case_id,
    }
    return request_header, request_body


def judge(src: str, language: str, test_case_id: str,
          max_cpu_time: int = 1000, max_memory: int = 134217728):
    config = judger_config.configs[language]
    header, body = build_judge_request(src, config, test_case_id, max_cpu_time, max_memory)
    result = requests.post(mjc_config.OJ_URL, headers=header, json=body)
    if result.status_code == 200:
        return result.json()
    else:
        raise Exception(f"Judge request failed with status code {result.status_code}")


def build_test_point_info(case_name: str, in_path: str, out_path: str):
    input_name = in_path.split('/')[-1]
    output_name = out_path.split('/')[-1]

    with open(in_path, 'r', encoding='utf-8') as f:
        input_ = f.read()
        input_size = len(input_.encode('utf-8'))
    with open(out_path, 'r', encoding='utf-8') as f:
        output = f.read()
        output_size = len(output.encode('utf-8'))
    output = output.strip()
    md.update(output.encode('utf-8'))

    return case_name.split('/')[-1], {
            "stripped_output_md5": md.hexdigest(),
            "output_size": output_size,
            "input_name": input_name,
            "input_size": input_size,
            "output_name": output_name,
        }


def build_test_case_info(path: str):
    in_files = glob.glob(os.path.join(path, '*.in'))
    out_files = glob.glob(os.path.join(path, '*.out'))

    # 配对 input 和 output
    in_files = map(lambda x: x.removesuffix('.in'), in_files)
    out_files = map(lambda x: x.removesuffix('.out'), out_files)
    samples = set(in_files) & set(out_files)
    test_cases = {}

    for sample in samples:
        in_path, out_path = sample + '.in', sample + '.out'
        k, v = build_test_point_info(sample, in_path, out_path)
        test_cases[k] = v

    return { "spj": False, "test_cases": test_cases }


def extract_test_cases(path: str, test_case_id: int):
    extract_path = os.path.join(os.path.dirname(path), str(test_case_id))
    shutil.unpack_archive(path, extract_path)

    info = build_test_case_info(extract_path)
    with open(os.path.join(extract_path, 'info'), 'w', encoding='utf-8') as f:
        json.dump(info, f)
    shutil.move(extract_path, mjc_config.OJ_TESTCASE_URL)
    return extract_path, info


def translate_judge_result(result_id: int):
    return judge_result[result_id]