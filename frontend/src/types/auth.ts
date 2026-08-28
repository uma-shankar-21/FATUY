export interface LoginRequest {
  identifier: string;
  password: string;
}

export interface Customer {
    id: string;

    username: string;

    email: string;

    first_name: string;

    last_name: string;

    phone: string;

    date_of_birth: string | null;

    is_active: boolean;

    created_at?: string;

    updated_at?: string;
}

export interface LoginResponse {
  message: string;

  access_token: string;

  token_type: string;

  customer: Customer;
}