import React, { createContext, useState, useEffect, useContext } from 'react';
import { authService } from '../services/api';

// Создание контекста аутентификации
const AuthContext = createContext();

// Компонент-провайдер аутентификации
export const AuthProvider = ({ children }) => {
    // Состояние для отслеживания статуса аутентификации
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    // Состояние для отслеживания процесса проверки аутентификации
    const [isLoading, setIsLoading] = useState(true);
    // Данные о пользователе
    const [userData, setUserData] = useState(null);

    // При первой загрузке проверяем. аутентифицирован ли пользователь
    useEffect(() => {
        const checkAuth = () => {
            const isAuth = authService.isAuthenticated();
            setIsAuthenticated(isAuth);
            
            // Если аутентифицирован, получаем данные пользователя
            if (isAuth) {
                const user = authService.getUserData();
                setUserData(user);
            }
            setIsLoading(false);
        };

        checkAuth();
    }, []);

    // Вход в систему
    const login = async (username, password) => {
        try {
            await authService.login(username, password);
            setIsAuthenticated(true);

            // После успешного входа получаем данные пользователя
            const user = authService.getUserData();
            setUserData(user);

            return true;
        } catch (error) {
            console.error('Login error:', error);
            return false;
        }
    };

    // Выход из системы
    const logout = () => {
        authService.logout();
        setIsAuthenticated(false);
        setUserData(null); // Очистка данных пользователя при выходе
    };

    // Значение контекста, которое будет доступно
    const value = {
        isAuthenticated,
        isLoading,
        userData,
        login,
        logout,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
};

// Хук для использования контекста аутентификации
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};