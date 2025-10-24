"use client";

import { useAdminUsers } from "@/lib/hooks/useAdminUsers";
import SetOrganizerRoleButton from "../buttons/admin-buttons/SetOrganizerRoleButton";

export default function UsersTable() {
  const { users, refetch, loading, error } = useAdminUsers();

  if (loading) return <p>Ładowanie...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <table className="admin-table">
      <thead>
        <tr>
          <th>Email</th>
          <th>Imię</th>
          <th>Nazwisko</th>
          <th>Organizator</th>
          <th>Akcja</th>
        </tr>
      </thead>
      <tbody>
        {users.map((u) => (
          <tr key={u.id}>
            <td>{u.email}</td>
            <td>{u.first_name || "-"}</td>
            <td>{u.last_name || "-"}</td>
            <td>{u.is_organizer ? "✅ Tak" : "❌ Nie"}</td>
            <td>
              <SetOrganizerRoleButton
                userId={u.id}
                isOrganizer={u.is_organizer}
                onDone={refetch}
              />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
