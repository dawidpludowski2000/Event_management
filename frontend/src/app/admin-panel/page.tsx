"use client";

import "./admin-panel.css";
import UsersTable from "@/components/admin/UserTable";

export default function AdminPanelPage() {
  return (
    <div className="admin-container">
      <h1 className="admin-title">Panel administratora</h1>
      <UsersTable />
    </div>
  );
}
