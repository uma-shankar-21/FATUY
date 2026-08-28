export interface BankAccount {
  id: string;

  customer_id: string;

  account_number: string;

  account_type: string;

  currency: string;

  balance: number;

  status: string;
}

export interface CustomerDashboard {
  customer: {
    id: string;

    username: string | null;

    email: string | null;

    first_name: string;

    last_name: string;

    phone: string;

    date_of_birth: string | null;
  };

  accounts: BankAccount[];
}