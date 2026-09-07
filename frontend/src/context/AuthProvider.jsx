import { useState } from 'react';
import authService from '../services/authService';
import api from '../services/api';
import { AuthContext } from './AuthContext';

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        const currentUser = authService.getCurrentUser();
        return currentUser && authService.isAuthenticated() ? currentUser : null;
    });
    const [loading] = useState(false);

    const login = async (username, password) => {
        try {
            await authService.getTokens(username, password);
            const response = await api.post('/auth/login/', { username, password });

            if (response.data.user) {
                localStorage.setItem('user', JSON.stringify(response.data.user));
                setUser(response.data.user);
                return { success: true };
            }
            return { success: false, error: 'Ошибка входа' };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.detail || 'Неверный логин или пароль',
            };
        }
    };

    const register = async (username, email, password, password2) => {
        await authService.register(username, email, password, password2);
        return await login(username, password);
    };

    const logout = () => {
        authService.logout();
        setUser(null);
    };

    const value = {
        user,
        loading,
        register,
        login,
        logout,
        isAuthenticated: !!user && authService.isAuthenticated(),
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};