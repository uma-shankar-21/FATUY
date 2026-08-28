import {
  useAuth,
} from "../../context/AuthContext";


export default function DashboardHeader() {

  const {
    customer,
    logout,
  } = useAuth();


  return (

    <header className="dashboard-header">

      <div>

        <p className="dashboard-eyebrow">
          PERSONAL BANKING
        </p>

        <h1>
          Good to see you,
          {" "}
          {customer?.first_name}
        </h1>

      </div>


      <div className="header-actions">

        <div className="user-avatar">

          {customer?.first_name
            ?.charAt(0)
            .toUpperCase()}

        </div>


        <button
          onClick={logout}
          className="logout-button"
        >
          Logout
        </button>

      </div>

    </header>

  );
}