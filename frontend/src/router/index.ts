import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsView.vue'),
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchView.vue'),
    },
    {
      path: '/progress',
      name: 'progress',
      component: () => import('../views/ProgressView.vue'),
    },
    {
      path: '/user/:username', //用户首页
      name: 'user',
      component: () => import('../views/UserView.vue'),
    },
    {
      path: '/user/:username/collections',
      name: 'user_collections',
      component: () => import('../views/UserCollectionsView.vue'),
    },
    {
      path: '/user/:username/mono',
      name: 'user_mono',
      component: () => import('../views/UserMonoView.vue'),
    },
    {
      path: '/user/:username/blog',
      name: 'user_blog',
      component: () => import('../views/UserBlogView.vue'),
    },
    {
      path: '/user/:username/index', // 用户目录
      name: 'user_index',
      component: () => import('../views/UserIndexView.vue'),
    },
    {
      path: '/user/:username/timeline',
      name: 'user_timeline',
      component: () => import('../views/UserTimelineView.vue'),
    },
    {
      path: '/user/:username/groups',
      name: 'user_groups',
      component: () => import('../views/UserGroupsView.vue'),
    },
    {
      path: '/user/:username/friends',
      name: 'user_friends',
      component: () => import('../views/UserFriendsView.vue'),
    },
    {
      path: '/user/:username/wiki',
      name: 'user_wiki',
      component: () => import('../views/UserWikiView.vue'),
    },
    {
      path: '/user_settings',
      name: 'user_settings',
      component: () => import('../views/UserSettingsView.vue'),
    },
    {
      path: '/subject/:id',
      name: 'subject',
      component: () => import('../views/SubjectView.vue'),
    },
  ],
})

export default router
