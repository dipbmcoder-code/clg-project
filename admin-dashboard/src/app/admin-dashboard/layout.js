'use client';

import PropTypes from 'prop-types';

import { RoleBasedGuard } from 'src/auth/guard';
import AdminDashboardLayout from 'src/layouts/admin-dashboard';

// ----------------------------------------------------------------------

export default function Layout({ children }) {
  return (
    <RoleBasedGuard roles={['Admin','Super Admin']} hasContent>
      <AdminDashboardLayout>{children}</AdminDashboardLayout>
    </RoleBasedGuard>
  );
}

Layout.propTypes = {
  children: PropTypes.node,
};
