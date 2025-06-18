export const API_CONFIG = {
  baseURL: 'http://localhost:8000/api/v1',
  endpoints: {
    auth: {
      login: '/auth/login/access-token',
      refresh: '/auth/login/refresh-token',
      register: '/auth/register',
      passwordRecovery: '/auth/password-recovery/:email',
      resetPassword: '/auth/reset-password',
      confirmEmail: '/auth/confirm-email/:token',
      changePassword: '/auth/reset-password-logged-user/'
    },
    users: {
      register: '/users/',
      me: '/users/me',
    },
    guests: {
      list: '/guests/me/',
      create: '/guests/',
      update: '/guests/:guest_id/',
      delete: '/guests/:guest_id/',
      send_invitations: '/guests/send_invitation_all_guests_not_confirmed',
      statistics: '/guests/statistics/me',
    },
  },
  tokenRefreshInterval: parseInt(process.env.REACT_APP_TOKEN_REFRESH_INTERVAL || '900000', 10), // 15 minutos por padrão
};