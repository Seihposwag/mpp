import axios from "axios";

const API_URL = "http://localhost:8000/api";

const authService = {
  // Регистрация
  async register(username, email, password, password2) {
    const response = await axios.post(`${API_URL}/auth/register/`, {
      username,
      email,
      password,
      password2,
    });
    return response.data;
  },

  // Вход
  async login(username, password) {
    const response = await axios.post(`${API_URL}/auth/login/`, {
      username,
      password,
    });

    if (response.data.user) {
      localStorage.setItem("user", JSON.stringify(response.data.user));
    }

    return response.data;
  },

  // Получение JWT токенов
  async getTokens(username, password) {
    const response = await axios.post(`${API_URL}/token/`, {
      username,
      password,
    });

    if (response.data.access) {
      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);
    }

    return response.data;
  },

  // Обновление access токена
  async refreshToken() {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) return null;

    try {
      const response = await axios.post(`${API_URL}/token/refresh/`, {
        refresh,
      });

      if (response.data.access) {
        localStorage.setItem("access_token", response.data.access);
      }

      return response.data;
    } catch (error) {
      console.error(error);
      this.logout();
      return null;
    }
  },

  // Выход
  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  },

  // Получение текущего пользователя
  getCurrentUser() {
    const userStr = localStorage.getItem("user");
    if (userStr) {
      return JSON.parse(userStr);
    }
    return null;
  },

  // Проверка авторизации
  isAuthenticated() {
    return !!localStorage.getItem("access_token");
  },
};

export default authService;
