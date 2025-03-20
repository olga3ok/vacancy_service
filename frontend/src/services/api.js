import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Создание экземпляра axios
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

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

        const response = await axios.post(`${API_URL}/auth/token`, formData, {
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

    fetchUserData: async () => {
        try {
            const response = await api.get('auth/me');
            console.log(response.data);
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
        const response = await api.get('/api/v1/vacancies/list');
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

    refreshFromHH: async (id) => {
        const response = await api.post(`/api/v1/vacancy/refresh-from-hh/${id}`);
        return response.data;
    }
};

export default api;