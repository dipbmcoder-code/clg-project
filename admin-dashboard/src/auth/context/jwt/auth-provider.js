'use client';

import PropTypes from 'prop-types';
import { useMemo, useEffect, useReducer, useCallback } from 'react';

import axios, { endpoints } from 'src/utils/axios';

import { AuthContext } from './auth-context';
import { getCookie, setCookie, setSession } from './utils';

const initialState = {
  user: null,
  loading: true,
};

const reducer = (state, action) => {
  if (action.type === 'INITIAL') {
    return {
      loading: false,
      user: action.payload.user,
    };
  }
  if (action.type === 'LOGIN') {
    return {
      ...state,
      user: action.payload.user,
    };
  }
  if (action.type === 'LOGOUT') {
    return {
      ...state,
      user: null,
    };
  }
  return state;
};

// ----------------------------------------------------------------------

const STORAGE_KEY = 'accessToken';

// Map backend role enum to display name expected by RoleBasedGuard
const ROLE_DISPLAY_MAP = {
  SUPER_ADMIN: 'Super Admin',
  ADMIN: 'Admin',
  AGENT: 'Agent',
};

const normalizeRole = (role) => ROLE_DISPLAY_MAP[role] || role;

export function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  const initialize = useCallback(async () => {
    try {
      const token = getCookie(STORAGE_KEY);

      if (token) {
        setSession(token);
        const response = await axios.get(endpoints.auth.me);
        const user = response.data.data;

        // Normalize user for role-based guard compatibility
        const normalizedUser = {
          ...user,
          token,
          roles: [{ name: normalizeRole(user.role) }],
        };

        dispatch({
          type: 'INITIAL',
          payload: {
            user: normalizedUser,
          },
        });
      } else {
        dispatch({
          type: 'INITIAL',
          payload: {
            user: null,
          },
        });
      }
    } catch (error) {
      console.error(error);
      dispatch({
        type: 'INITIAL',
        payload: {
          user: null,
        },
      });
    }
  }, []);

  useEffect(() => {
    initialize();
  }, [initialize]);

  // LOGIN
  const login = useCallback(async (email, password) => {
    const data = {
      email,
      password,
    };
    const response = await axios.post(endpoints.auth.login, data);

    const { token, user } = response.data.data;
    setSession(token);
    setCookie(STORAGE_KEY, token, 3);

    // Normalize user object for role-based guard compatibility
    const normalizedUser = {
      ...user,
      token,
      roles: [{ name: normalizeRole(user.role) }],
    };

    dispatch({
      type: 'LOGIN',
      payload: {
        user: normalizedUser,
      },
    });
  }, []);

  // LOGOUT
  const logout = useCallback(async () => {
    setSession(null);
    dispatch({
      type: 'LOGOUT',
    });
  }, []);

  // ----------------------------------------------------------------------

  const checkAuthenticated = state.user ? 'authenticated' : 'unauthenticated';

  const status = state.loading ? 'loading' : checkAuthenticated;

  const memoizedValue = useMemo(
    () => ({
      user: state.user,
      method: 'jwt',
      loading: status === 'loading',
      authenticated: status === 'authenticated',
      unauthenticated: status === 'unauthenticated',
      //
      login,
      logout,
    }),
    [login, logout, state.user, status]
  );

  return <AuthContext.Provider value={memoizedValue}>{children}</AuthContext.Provider>;
}

AuthProvider.propTypes = {
  children: PropTypes.node,
};
