import { createRouter, createWebHistory } from 'vue-router'
import OcrView from '@/views/OcrView.vue'
import FinalPriceView from '@/views/FinalPriceView.vue'
import priceHistory from '@/views/HistoryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'ocr', component: OcrView },
    { path: '/final', name: 'final', component: FinalPriceView },
    { path: '/history', name: 'history', component: priceHistory },
  ],
})

export default router
