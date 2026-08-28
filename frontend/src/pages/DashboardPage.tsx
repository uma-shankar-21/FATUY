import { useEffect, useState } from "react";

import DashboardHeader from "../components/dashboard/DashboardHeader";

import AccountCard from "../components/dashboard/AccountCard";

import CustomerProfile from "../components/dashboard/CustomerProfile";

import ChatPanel from "../components/chat/ChatPanel";

import { getCustomerDashboard } from "../api/customer";

import type { BankAccount } from "../types/customer";

import { useAuth } from "../context/AuthContext";

export default function DashboardPage() {
  const { customer } = useAuth();

  const [accounts, setAccounts] = useState<BankAccount[]>([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const data = await getCustomerDashboard();

        console.log("DASHBOARD API RESPONSE:", data);

        setAccounts(Array.isArray(data.accounts) ? data.accounts : []);
      } catch (error) {
        console.error("Failed to load dashboard", error);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

const totalBalance =
    (accounts || []).reduce(
        (
            total,
            account
        ) =>
            total +
            Number(account.balance),

        0
    );

  return (
    <div className="dashboard-layout">
      <main className="dashboard-main">
        <DashboardHeader />

        <section className="dashboard-overview">
          <div className="total-balance-card">
            <span>Total available balance</span>

            <h2>
              ₹
              {totalBalance.toLocaleString("en-IN", {
                minimumFractionDigits: 2,
              })}
            </h2>

            <p>Across all active accounts</p>
          </div>

          {customer && <CustomerProfile customer={customer} />}
        </section>

        <section className="accounts-section">
          <div className="section-header">
            <div>
              <p>YOUR BANKING</p>

              <h2>Accounts</h2>
            </div>
          </div>

          {loading ? (
            <div className="dashboard-loading">Loading your accounts...</div>
          ) : accounts.length === 0 ? (
            <div className="empty-state">No accounts found.</div>
          ) : (
            <div className="accounts-grid">
              {accounts.map((account) => (
                <AccountCard key={account.id} account={account} />
              ))}
            </div>
          )}
        </section>
      </main>

      <ChatPanel />
    </div>
  );
}
