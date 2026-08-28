import {
    useState,
    type FormEvent,
} from "react";

import {
    useNavigate,
} from "react-router-dom";

import {
    useAuth,
} from "../context/AuthContext";

import apiClient
    from "../api/client";


export default function LoginPage() {

    const navigate =
        useNavigate();


    const {
        login,
    } = useAuth();


    const [
        identifier,
        setIdentifier,
    ] = useState(
        ""
    );


    const [
        password,
        setPassword,
    ] = useState(
        ""
    );


    const [
        error,
        setError,
    ] = useState(
        ""
    );


    const [
        loading,
        setLoading,
    ] = useState(
        false
    );


    async function handleSubmit(
        event: FormEvent<HTMLFormElement>
    ) {

        event.preventDefault();


        if (
            !identifier.trim() ||
            !password
        ) {

            setError(
                "Username/email and password are required."
            );

            return;

        }


        try {

            setLoading(
                true
            );

            setError(
                ""
            );


            const response =
                await apiClient.post(
                    "/auth/login",
                    {
                        identifier:
                            identifier.trim(),

                        password,
                    }
                );


            console.log(
                "LOGIN RESPONSE:",
                response.data
            );


            const {
                access,
                customer,
            } = response.data;


            if (
                !access ||
                !customer
            ) {

                throw new Error(
                    "Invalid login response."
                );

            }


            login(
                access,
                customer
            );


            console.log(
                "NAVIGATING TO DASHBOARD"
            );


            navigate(
                "/dashboard",
                {
                    replace: true,
                }
            );

        } catch (
            error: any
        ) {

            console.error(
                "LOGIN ERROR:",
                error
            );


            const detail =
                error?.response
                    ?.data
                    ?.detail;


            setError(

                typeof detail ===
                    "string"

                    ? detail

                    : "Invalid username/email or password."

            );

        } finally {

            setLoading(
                false
            );

        }

    }


    return (

  <div className="login-page">

    <div className="login-card">

      <div className="login-brand">

        <div className="login-logo">
          B
        </div>

        <h1>
          Banking AI
        </h1>

        <p>
          Secure intelligent banking
        </p>

      </div>


      <h2>
        Welcome back
      </h2>

      <p className="login-subtitle">
        Sign in to access your banking dashboard.
      </p>


      <form
        className="login-form"
        onSubmit={handleSubmit}
      >

        <div className="form-group">

          <label>
            Username or Email
          </label>

          <input
            type="text"
            placeholder="Enter username or email"
            value={identifier}
            onChange={(event) =>
              setIdentifier(
                event.target.value
              )
            }
          />

        </div>


        <div className="form-group">

          <label>
            Password
          </label>

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) =>
              setPassword(
                event.target.value
              )
            }
          />

        </div>


        {error && (

          <div className="login-error">
            {error}
          </div>

        )}


        <button
          type="submit"
          className="login-button"
          disabled={loading}
        >

          {loading
            ? "Signing in..."
            : "Sign in"}

        </button>

      </form>

    </div>

  </div>

);

}