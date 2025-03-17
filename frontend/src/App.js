import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

import LoginPage from './pages/LoginPage';
import VacancyListPage from './pages/VacancyListPage';
import VacancyDetailPage from './pages/VacancyDetailPage';
import VacancyCreatePage from './pages/VacancyCreatePage';
import VacancyEditPage from './pages/VacancyEditPage';
import Layout from './components/Layout/Layout';

// Компонент защищенного маршрута - проверяет аутентификацию пользователя
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  // Показывает индикатор загрузки, пока проверяется аутентификация
  if (isLoading) {
    return <div className="d-flex justify-content-center mt-5">Loading...</div>;
  }

  // Если пользователь не аутентифицирован, перенаправляем на страницу логина
  if (!isAuthenticated) {
    return <Navigate to="/login" />
  }

  // Если пользователь аутентифицирован, отображаем запрашиваемый компонет
  return children;
};

function App() {
  return (
    // Оборачивание приложения в провайдер аутентификации
    <AuthProvider>
      {/* Настройка роутинга */}
      <Router>
        <Routes>
          {/* Публичный маршрут для страницы входа */}
          <Route path="/login" element={<LoginPage />} />
          
          {/* Защищенный маршрут для главной страницы */}
          <Route path="/" element={
            <ProtectedRoute>
              <Layout>
                <VacancyListPage />
              </Layout>
            </ProtectedRoute>
          } />
          
          {/* Защищенные маршруты для создания, просмотра и редактирования вакансий */}
          <Route path="/vacancies/create" element={
            <ProtectedRoute>
              <Layout>
                <VacancyCreatePage />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/vacancies/:id" element={
            <ProtectedRoute>
              <Layout>
                <VacancyDetailPage />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/vacancies/:id/edit" element={
            <ProtectedRoute>
              <Layout>
                <VacancyEditPage />
              </Layout>
            </ProtectedRoute>
          } />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
