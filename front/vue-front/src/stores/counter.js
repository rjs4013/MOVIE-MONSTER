import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import LogInView from '@/views/LogInView.vue'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const rankings = ref([]); // 랭킹 데이터를 저장
  const Username = ref(null)  // 사용자 이름 저장 변수 추가
  // const user = ref({ username: '', points: 0 }); // 유저 정보
  const user = ref({});
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()
  const signUpResponse = ref(null); // 회원가입 성공/실패 응답 데이터 저장
  const error = ref(null); // 에러 메시지 저장

  // 서버에서 데이터 가져오기
  const fetchArticles = async () => {
    console.log("fetchArticles function invoked"); // 함수 호출 확인
    try {
      const response = await axios.get(`${API_URL}/api/v1/communities/`, {
        headers: { Authorization: `Token ${token.value}` },
      })
      console.log("Articles with comment count:", response.data); // comment_count 확인
      articles.value = response.data
      console.log('ppaaaa',articles.value)
    } catch (error) {
      console.error('Error fetching articles:', error)
    }
  }

  // 회원가입 함수
  const signUp = async (payload) => {
    try {
      const response = await axios.post(`${API_URL}/accounts/custom-signup/`, payload, {
        headers: {
          'Content-Type': 'multipart/form-data', // FormData 처리
        },
      });
      signUpResponse.value = response.data; // 회원가입 성공 응답 데이터 저장
      console.log("회원가입 성공:", response.data);
  
      // 회원가입 성공 후 자동으로 로그인 처리
      const loginPayload = {
        username: payload.get("username"), // FormData에서 username 가져오기
        password: payload.get("password1"), // password1 가져오기
      };
      await logIn(loginPayload); // 로그인 처리
  
      // 로그인 성공 후 홈으로 이동
      router.push({ name: "HomeView" });
    } catch (err) {
      error.value = err.response?.data || err.message; // 실패 시 에러 저장
      console.error("회원가입 실패:", error.value);
      throw err; // 에러 재발생
    }
  };
  

  // 클라이언트 정렬 로직
  const sortArticles = (sortOrder) => {
    if (sortOrder === 'popular') {
      articles.value.sort((a, b) => b.like_count - a.like_count) // 좋아요 많은 순
    } else if (sortOrder === 'recent') {
      console.log('a',articles.value)
      articles.value.sort((a, b) => b.id - a.id); // id 내림차순
    }
  }

  // 정렬된 데이터 가져오기
  const getSortedArticles = async (sortOrder = "recent") => {
    // if (!articles.value.length) {
    //   console.log("Fetching articles from server...");
      await fetchArticles();
    // }
    console.log('111',articles.value)
  
    // 정렬만 수행
    sortArticles(sortOrder);
  };

  // 날짜 포맷팅 함수 추가
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day} ${hours}:${minutes}`
  }

  // 랭킹 데이터를 가져오는 함수
  const fetchRankings = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/communities/ranking/`, {
        headers: { Authorization: `Token ${token.value}` },
      });
      rankings.value = response.data;
      console.log('Fetching rankings...', rankings.value);
      console.log('Rankings fetched:', response.data);
    } catch (error) {
      console.error('Error fetching rankings:', error);
    }
  };

  // 별점 표시 함수
  const displayStars = (rating) => {
    const stars = []
    for (let i = 1; i <= 10; i++) {
      stars.push({
        filled: i <= rating, // rating 이하의 별은 노란색으로 채워짐
      })
    }
    return stars
  }

  const syncArticle = (updatedArticle) => {
    const index = articles.value.findIndex((a) => a.id === updatedArticle.id);
    if (index !== -1) {
      articles.value[index] = { ...articles.value[index], ...updatedArticle };
    }
  };

  //////////////////////////////////////////////
  const fetchUser = async () => {
    try {
      const response = await axios.get(`${API_URL}/accounts/user/`, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      user.value = { ...response.data, id: response.data.pk }; // 사용자 정보 저장
      Username.value = response.data.username;
      //->개빡치네
      //백엔드에서 사용자 ID를 pk로 보내주는데, 프론트엔드에서는 id로 사용하려고 했기 때문임
      console.log("User fetched:", user.value);
    } catch (error) {
      console.error("Error fetching user:", error);
      user.value = {};
    }
  };
  // axios 요청 공통 헤더 설정 (인터셉터 사용)
axios.defaults.headers.common['Authorization'] = () => `Token ${token.value}`;

  
  // 카테고리 이름 수정
  const updateCategoryName = async (categoryId, newName) => {
    try {
      const response = await axios.patch(
        `${API_URL}/accounts/categories/${categoryId}/update/`,
        { name: newName },
        {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        }
      );
      console.log("Category name updated:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error updating category name:", error);
      throw error;
    }
  };

  // 카테고리 삭제
  const deleteCategory = async (categoryId) => {
    try {
      await axios.delete(`${API_URL}/accounts/categories/${categoryId}/delete/`, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      console.log("Category deleted successfully.");
    } catch (error) {
      console.error("Error deleting category:", error);
      throw error;
    }
  };

  // 카테고리에서 영화 삭제
  const removeMovieFromCategory = async (categoryId, movieId) => {
    try {
      await axios.post(
        `${API_URL}/accounts/categories/remove-movie/`,
        { category_id: categoryId, movie_id: movieId },
        {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        }
      );
      console.log("Movie removed from category successfully.");
    } catch (error) {
      console.error("Error removing movie from category:", error);
      throw error;
    }
  };
  //////////////////////////////////////////////

  // 랭크 계산 함수
  const getRankTitle = (points) => {
    if (points < 1000) return "Bronze";
    if (points < 2000) return "Silver";
    if (points < 3000) return "Gold";
    if (points < 4000) return "Platinum";
    return "Diamond";
  };

  
  const fetchUserPoints = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/accounts/user/points/`, {
        headers: {
          Authorization: `Token ${token.value}`, // JWT 토큰 추가
        },
      });
      console.log(response.data)
      user.value = {
        ...user.value, // 기존 사용자 데이터 유지
        current_points: response.data.current_points,
        rank_title: getRankTitle(response.data.current_points),
      };
      // fetchRankings 함수에서 데이터를 로깅합니다.
      console.log('Rankings fetched:', response.data);

    } catch (error) {
      console.error('Error fetching user points:', error);
    }
  };

  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
  const getArticles = (forceReload = false) => {
    console.log("getArticles function called");
  
    if (!forceReload && articles.value.length > 0) {
      console.log('qwe',articles.value)
      console.log("Articles already loaded, skipping reload");
      return;
    }
  
    axios({
      method: "get",
      url: `${API_URL}/api/v1/communities/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then((response) => {
        articles.value = response.data; // 데이터를 Vue의 반응형 상태로 설정
        console.log("Updated articles:", articles.value);
      })
      .catch((err) => {
        console.error("Error fetching articles:", err);
      });
  };


  // 회원가입 요청 액션
  // const signUp = function (payload) {
  //   // const username = payload.username
  //   // const password1 = payload.password1
  //   // const password2 = payload.password2
  //   const { username, password1, password2 } = payload

  //   axios({
  //     method: 'post',
  //     url: `${API_URL}/accounts/signup/`,
  //     data: {
  //       username, password1, password2
  //     }
  //   })
  //     .then((res) => {
  //       // console.log(res)
  //       // console.log('회원가입 성공')
  //       const password = password1
  //       logIn({ username, password })
  //       // console.log("로그인됐나요?:", isLogin)
  //     })
  //     .then(() => {
  //       fetchUserPoints(); // 로그인 이후 즉시 사용자 포인트 정보를 가져옴
  //     })
  //     .catch((err) => {
  //       console.log(err)
  //     })
  //   }

  // // 로그인 요청 액션
  // const logIn = function (payload) {
  //   // const username = payload.username
  //   // const password1 = payload.password
  //   const { username, password } = payload

  //   axios({
  //     method: 'post',
  //     url: `${API_URL}/accounts/login/`,
  //     data: {
  //       username, password
  //     }
  //   })
  //     .then((res) => {
  //       token.value = res.data.key;
  //       // 사용자 정보를 가져오는 추가 요청
  //       axios({
  //         method: 'get',
  //         url: `${API_URL}/accounts/user/`,  // 사용자 정보를 가져오는 엔드포인트
  //         headers: {
  //           Authorization: `Token ${token.value}`
  //         }
  //       })

  //         .then((userRes) => {
  //           console.log(userRes.data)
  //           Username.value = userRes.data.username  // 사용자 이름 저장
  //           router.push({ name: 'HomeView' })
  //         })
  //         .catch((err) => {
  //           console.log('Error fetching user information:', err)
  //         })
  //       return fetchUserPoints()
  //     })
  //     .catch((err) => {
  //       console.log(err)
  //     })
  // }
  const logIn = async function (payload) {
    try {
      const { username, password } = payload;
      const res = await axios.post(`${API_URL}/accounts/login/`, {
        username,
        password,
      });
      token.value = res.data.key; // 토큰 저장
  
      await fetchUser(); // 사용자 정보 비동기 로드
      await fetchUserPoints(); // 포인트 정보 업데이트
  
      router.push({ name: "HomeView" }); // 홈페이지로 리다이렉트
    } catch (err) {
      console.error("Login error:", err);
      alert("로그인에 실패했습니다. 사용자 이름과 비밀번호를 확인해주세요.");
    }
  };
  
  
  // [추가기능] 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        token.value = null
        Username.value = null  // 로그아웃 시 사용자 이름 초기화
        localStorage.removeItem('token')  // 로컬 스토리지에서 토큰 제거
        user.value = { username: '', points: 0 } // 유저 정보 초기화
        router.push({ name: 'ArticleView' }) // 로그아웃 후 리다이렉트
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 댓글 작성 및 댓글 목록 요청을 위한 함수 추가
  const getComments = (articleId) => {
    return axios({
      method: 'get',
      url: `${API_URL}/api/v1/communities/${articleId}/comments/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
  }

  const addComment = (articleId, commentContent) => {
    return axios({
      method: 'post',
      url: `${API_URL}/api/v1/communities/${articleId}/comments/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: { content: commentContent }
    })
  }

    // 댓글 수정 API 호출
  const updateComment = (articleId, commentId, updatedContent) => {
    return axios({
      method: 'put',
      url: `${API_URL}/api/v1/communities/${articleId}/comments/${commentId}/update/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
      data: { content: updatedContent },
    });
  };

  // 댓글 삭제 API 호출
  const deleteComment = (articleId, commentId) => {
    return axios({
      method: 'delete',
      url: `${API_URL}/api/v1/communities/${articleId}/comments/${commentId}/delete/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
    });
  };

  const fetchCategoryDetails = async (categoryId) => {
    const response = await axios.get(`${API_URL}/accounts/categories/${categoryId}/`, {
      headers: { Authorization: `Token ${token.value}` },
    });
    return response.data; // { category: { ... }, movies: [ ... ] }
  };

  const searchMovies = async (title) => {
    const response = await axios.get(`${API_URL}/accounts/movies/search/`, {
      params: { title },
      headers: { Authorization: `Token ${token.value}` },
    });
    return response.data; // 검색된 영화 리스트 반환
  };


  const addMovieToCategory = async (categoryId, movieId) => {
    await axios.post(
      `${API_URL}/accounts/categories/add-movie/`,
      { category_id: categoryId, movie_id: movieId },
      { headers: { Authorization: `Token ${token.value}` } }
    );
    alert("영화가 카테고리에 추가되었습니다.");
  };

  const createArticle = async (articleData) => {
    try {
      console.log('bb',articleData)
      const response = await axios.post(`${API_URL}/api/v1/communities/`, articleData, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      console.log("Article created successfully:", response.data);
      
      return response.data;
    } catch (error) {
      console.error("Error creating article:", error);
      throw error;
    }
  };

  const updateLikeStatus = async (articleId) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/v1/communities/${articleId}/like/`,
        {}, // POST 요청의 body는 비워둠
        {
          headers: { Authorization: `Token ${token.value}` }, // headers는 config 안에 설정
        }
      );
  
      const updatedArticle = response.data;
  
      // articles 배열에서 해당 article을 업데이트
      const index = articles.value.findIndex((a) => a.id === articleId);
      if (index !== -1) {
        articles.value[index] = { ...articles.value[index], ...updatedArticle };
      }
  
      return updatedArticle;
    } catch (err) {
      console.error("좋아요 상태 업데이트 실패:", err);
      throw err;
    }
  };
  

  const getArticleDetail = async (articleId) => {
    const response = await axios.get(`${API_URL}/api/v1/communities/${articleId}/`,
      {
        headers: { Authorization: `Token ${token.value}` }, // headers를 올바르게 설정
      }
    );
    console.log('ㅅㅂ', response.data)
    return response.data;
  };
  return { 
    articles, 
    API_URL, 
    addComment, 
    getComments, 
    getArticles, 
    signUp, 
    logIn, 
    token, 
    isLogin, 
    logOut, 
    Username, 
    fetchUserPoints, 
    user, 
    fetchUser, // 사용자 정보 가져오기
    updateCategoryName, // 카테고리 이름 수정
    deleteCategory, // 카테고리 삭제
    removeMovieFromCategory, // 카테고리에서 영화 삭제
    displayStars, 
    fetchRankings, 
    rankings, 
    updateComment, 
    deleteComment,
    formatDate,
    getSortedArticles,
    signUp,
    signUpResponse,
    error,
    getRankTitle,
    fetchCategoryDetails,
    searchMovies,
    addMovieToCategory,
    createArticle,
    updateLikeStatus,
    syncArticle,
    getArticleDetail,
  }
}, { persist: true })