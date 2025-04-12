import axios from '../utils/request';

export interface LoginRequest {
    username: string;
    password: string;
}

export interface LoginResponse {
    access_token: string;
}

export const loginApi = (data: LoginRequest) => {
    return axios.post<LoginResponse>('/user/login', data);
};