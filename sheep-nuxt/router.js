import Vue from 'vue'
import VueRouter from 'vue-router'
import settings from '@/conf/settings'

Vue.use(VueRouter)

import app from './pages/app'
import index_vue from './pages/index_vue/index_vue'
import login from './pages/login/login'
import postings from './pages/postings/postings'

import index from './pages/index_vue/index/index'
import info from './pages/index_vue/info/info'
import my_post from './pages/index_vue/my_post/my_post'
import my_question from './pages/index_vue/my_question/my_question'

// import NotFound from './views/notFound/notFound'
// import test from './views/test/test'

// import setting from './conf/settings'


const routes = [
  // {
  //   path:'/',
  //   redirect:'/index_vue',
  // },
  {
    path:'',
    component:app,
    children:[
      // 首页模板
      {
        path: '',
        component: index_vue,
        meta:{
          keepAlive:true,
        },
        children:[
          {
            // 首页
            path:'index/',
            name:'index',
            component:index,
          },
          {
            // 个人信息
            path:'info/',
            name:'info',
            component:info,
            meta:{
              is_login:true
            }
          },
              {
                // 我的文章
                path:'my_post',
                name:'my_post',
                component:my_post,
                meta:{
                  is_login:true
                }
              },
              {
                path:'my_question',
                name:'my_question',
                component:my_question,
                meta:{
                  is_login:true
                }
              },
          {
            path:'',
            redirect:'index'
          }
        ]
      },
      {
        // 创建帖子
        path:'/postings/',
        name:'postings',
        component:postings,
        meta:{
          no_back_top:true,
          is_login:true
        }
      },
      {
        // 修改帖子
        path:'/postings/:id',
        name:'postings_detail',
        component:postings,
        meta:{
          no_back_top:true,
          is_login:true
        }
      },
      {
        path:'/login',
        name:'login',
        component: login,
        meta:{
        }
      },
      // {
      //   path:'/test',
      //   name:'test',
      //   component: test
      // },
      // {
      //   path:'*',
      //   component:NotFound
      // }
    ]
  },

]

export function createRouter () {
  const router = new VueRouter({
    mode: 'history',
    // base: process.env.BASE_URL,
    routes
  })
  router.beforeEach((to, from, next) => {
    if(to.meta.is_login){
      if(!process.$cookies.secure_get(settings.TOKEN_NAME)){
        next({
          path: '/login',
          query: {redirect: to.fullPath}   //登录成功后重定向到当前页面
        })
      }
    }
    next()
  })
  return router
}




