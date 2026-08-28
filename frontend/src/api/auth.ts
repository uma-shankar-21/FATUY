import apiClient from "./client";

import type {
  LoginRequest,
  LoginResponse,
} from "../types/auth";


export const login = async (
  data: LoginRequest
): Promise<LoginResponse> => {

  const response = await apiClient.post(
    "/auth/login",
    data
  );

  return response.data;
};