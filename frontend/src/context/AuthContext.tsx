import {
    createContext,
    useContext,
    useEffect,
    useState,
    type ReactNode,
} from "react";

import type {
    Customer,
} from "../types/auth";


interface AuthContextType {

    token: string | null;

    customer: Customer | null;

    loading: boolean;

    login: (
        accessToken: string,
        customerData: Customer,
    ) => void;

    logout: () => void;
}


const AuthContext =
    createContext<AuthContextType | undefined>(
        undefined
    );


interface AuthProviderProps {

    children: ReactNode;
}


export function AuthProvider({
    children,
}: AuthProviderProps) {

    const [token, setToken] =
        useState<string | null>(
            null
        );

    const [customer, setCustomer] =
        useState<Customer | null>(
            null
        );

    const [loading, setLoading] =
        useState(true);


    // ======================================================
    // RESTORE AUTH STATE
    // ======================================================

    useEffect(() => {

        try {

            const storedToken =
                localStorage.getItem(
                    "access_token"
                );

            const storedCustomer =
                localStorage.getItem(
                    "customer"
                );


            if (storedToken) {

                setToken(
                    storedToken
                );

            }


            if (storedCustomer) {

                setCustomer(
                    JSON.parse(
                        storedCustomer
                    )
                );

            }

        } catch (error) {

            console.error(
                "Failed to restore auth state:",
                error
            );

            localStorage.removeItem(
                "access_token"
            );

            localStorage.removeItem(
                "customer"
            );

        } finally {

            setLoading(
                false
            );

        }

    }, []);


    // ======================================================
    // LOGIN
    // ======================================================

    function login(
        accessToken: string,
        customerData: Customer,
    ) {

        console.log(
            "AUTH LOGIN SUCCESS"
        );

        localStorage.setItem(
            "access_token",
            accessToken
        );

        localStorage.setItem(
            "customer",
            JSON.stringify(
                customerData
            )
        );

        setToken(
            accessToken
        );

        setCustomer(
            customerData
        );

    }


    // ======================================================
    // LOGOUT
    // ======================================================

    function logout() {

        localStorage.removeItem(
            "access_token"
        );

        localStorage.removeItem(
            "customer"
        );

        setToken(
            null
        );

        setCustomer(
            null
        );

    }


    return (

        <AuthContext.Provider
            value={{
                token,
                customer,
                loading,
                login,
                logout,
            }}
        >

            {children}

        </AuthContext.Provider>

    );

}


export function useAuth() {

    const context =
        useContext(
            AuthContext
        );


    if (!context) {

        throw new Error(
            "useAuth must be used inside AuthProvider"
        );

    }


    return context;

}