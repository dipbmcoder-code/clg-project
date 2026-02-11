import PropTypes from 'prop-types';
import { useState, useEffect, useCallback } from 'react';

import { paths } from 'src/routes/paths';
import { useRouter } from 'src/routes/hooks';

import { View403 } from 'src/sections/error';

import { useAuthContext } from '../hooks';
// ----------------------------------------------------------------------

const loginPaths = {
  jwt: paths.auth.login,
};

// ----------------------------------------------------------------------

export default function RoleBasedGuard({ hasContent, roles, children, sx }) {
  const { loading } = useAuthContext();
  return (
    <>
      {loading ? (
        <></>
      ) : (
        <RoleContainer hasContent={hasContent} roles={roles} sx={sx}>
          {children}
        </RoleContainer>
      )}
    </>
  );
}

RoleBasedGuard.propTypes = {
  children: PropTypes.node,
  hasContent: PropTypes.bool,
  roles: PropTypes.arrayOf(PropTypes.string),
  sx: PropTypes.object,
};
// ----------------------------------------------------------------------

function RoleContainer({ hasContent, roles, children, sx }) {
  const router = useRouter();

  const { user, authenticated, method } = useAuthContext();

  const [checked, setChecked] = useState(false);
  const check = useCallback(() => {
    if (!authenticated) {
      const searchParams = new URLSearchParams({
        returnTo: window.location.pathname,
      }).toString();

      const loginPath = loginPaths[method];

      const href = `${loginPath}?${searchParams}`;

      router.replace(href);
    } else {
      setChecked(true);
    }
  }, [authenticated, method, router]);

  useEffect(() => {
    check();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!checked) {
    return null;
  }
  const currentRoles = user?.roles?.map((role) => role.name) || [];
  if (typeof roles !== 'undefined' && !roles.some((role) => currentRoles.includes(role))) {
    return hasContent && authenticated ? <View403 /> : null;
  }

  return <>{children}</>;
}

RoleContainer.propTypes = {
  children: PropTypes.node,
};
