import apiClient from "./client";

import type {
  CustomerDashboard,
} from "../types/customer";


export const getCustomerDashboard =
  async (): Promise<CustomerDashboard> => {

    const response = await apiClient.get(
      "/dashboard"
    );

    return response.data;
  };