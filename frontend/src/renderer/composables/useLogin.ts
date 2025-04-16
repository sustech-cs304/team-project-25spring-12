import {loginApi} from "../api/auth";
import {LoginRequest} from "../types/auth"

export function useLogin() {
    const login = async (param: LoginRequest) => {
        const formData = new FormData();
        formData.append("username", param.username);
        formData.append("password", param.password);

        const response = await loginApi(formData);
        return response.data;
    };

    return {
        login,
    };
}