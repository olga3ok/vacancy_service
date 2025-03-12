import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Создание экземпляра axios
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Декодирование JWT токена для получения информации о пользователе
const decodeToken = (token) => {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayLoad = decodeURIComponent(
            atob(base64)
                .split('')
                .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                .join('')
        );
        return JSON.parse(jsonPayLoad);
    } catch (e) {
        console.error('Error decoding token:', e);
        return null;
    }
};

// Добавление интерцептора запросов для добавления JWT токена к запросам
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Обработка 401 ответов перенаправлением на страницу логина
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Сервис аутентификации
export const authService = {
    login: async (username, password) => {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await axios.post(`${API_URL}/token`, formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
        }

        return response.data;
    },

    logout: () => {
        localStorage.removeItem('token');
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },

    getUserData: () => {
        const token = localStorage.getItem('token');
        if (!token) {
            return null;
        }

        const decodedToken = decodeToken(token);
        return decodedToken ? {
            id: decodedToken.sub,
            username: decodedToken.username || decodedToken.sub
        } : null;
    },

    fetchUserData: async () => {
        try {
            const response = await api.get('/api/v1/users/me');
            return response.data;
        } catch (error) {
            console.error('Failed to fetch user data:', error);
            return null;
        }
    }
};

// Сервис для работы с вакансиями
export const vacancyService = {
    getAll: async () => {
        const response = await api.get('/api/v1/vacancy/list');
        return response.data;
    },

    getById: async (id) => {
        const response = await api.get(`/api/v1/vacancy/get/${id}`);
        return response.data;
    },

    create: async (vacancyData) => {
        const response = await api.post('/api/v1/vacancy/create', vacancyData);
        return response.data;
    },

    createFromHH: async (hhId) => {
        const response = await api.post('/api/v1/vacancy/create', null, {
            params: { hh_id: hhId }
        });
        return response.data;
    },

    update: async (id, vacancyData) => {
        const response = await api.put(`/api/v1/vacancy/update/${id}`, vacancyData);
        return response.data;
    },

    delete: async (id) => {
        const response = await api.delete(`/api/v1/vacancy/delete/${id}`);
        return response.data;
    },
};

export default api;