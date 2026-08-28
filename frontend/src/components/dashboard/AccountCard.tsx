import type {
  BankAccount,
} from "../../types/customer";
import "./AccountCard.css";

interface AccountCardProps {
  account: BankAccount;
}


export default function AccountCard({
  account,
}: AccountCardProps) {

  const formattedBalance =
    new Intl.NumberFormat(
      "en-IN",
      {
        style: "currency",
        currency: account.currency,
        maximumFractionDigits: 2,
      }
    ).format(
      Number(account.balance)
    );


return (

  <div className="account-card">

    <div className="account-card-header">

      <span className="account-type">
        {account.account_type}
      </span>

      <span
        className={`account-status ${
          account.status === "ACTIVE"
            ? "active"
            : "inactive"
        }`}
      >
        {account.status}
      </span>

    </div>


    <div className="account-balance">

      {formattedBalance}

    </div>


    <div className="account-number">

      Account ••••
      {account.account_number.slice(-4)}

    </div>

  </div>

);
}