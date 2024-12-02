import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1", // Django API URL
  timeout: 10000, // 요청 시간 초과
  withCredentials: true, // 필요하면 사용 
});

// 요청 시 Authorization 헤더 추가
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("token"); // localStorage에서 토큰 가져오기
  if (token) {
    config.headers.Authorization = `Token ${token}`; // 헤더에 토큰 추가
  }
  return config;
});

export default axiosInstance;
