import type {
  Customer,
} from "../../types/auth";


interface CustomerProfileProps {
  customer: Customer;
}


export default function CustomerProfile({
  customer,
}: CustomerProfileProps) {

  return (

    <div className="customer-profile">

      <div className="profile-avatar">

        {customer.first_name
          .charAt(0)
          .toUpperCase()}

        {customer.last_name
          .charAt(0)
          .toUpperCase()}

      </div>


      <div className="profile-info">

        <h3>
          {customer.first_name}{" "}
          {customer.last_name}
        </h3>

        <span>
          {customer.email}
        </span>

      </div>

    </div>

  );
}