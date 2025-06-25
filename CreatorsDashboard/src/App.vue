<template>
  <div class="container my-4 custom-background text-white">
    <h1 class="text-center mb-4">Dashboard</h1>

    <ul class="nav nav-tabs mb-3">
      <li class="nav-item">
        <button class="nav-link" :class="{ active: activeTab === 'resume' }" @click="setTab('resume')">Content Type Resume</button>
      </li>
      <li class="nav-item">
        <button class="nav-link" :class="{ active: activeTab === 'other' }" @click="setTab('other')">All Creators</button>
      </li>
    </ul>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-if="activeTab === 'resume'">
      <div class="mb-3">
        <input v-model="searchText" type="text" class="form-control" placeholder="Search by Content Type name..." />
      </div>

      <div class="mb-3">
        <select v-model="sortOrder" class="form-select">
          <option value="desc">Followers Descending</option>
          <option value="asc">Followers Ascending</option>
        </select>
      </div>

      <table class="table table-striped table-bordered table-dark">
        <thead class="table-secondary text-center">
          <tr>
            <th>Content Type</th>
            <th>Total Followers</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in sortedAndFiltered" :key="item.contentType">
            <td class="text-center">{{ item.contentType }}</td>
            <td class="text-center">{{ item.totalFollowers }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="activeTab === 'other'">
      <h3>All Creators</h3>

      <div class="mb-3">
        <input v-model="creatorSearchText" type="text" class="form-control" placeholder="Search by Creator Name..." />
      </div>

      <div class="mb-3 d-flex gap-2">
        <select v-model="orderField" class="form-select">
          <option value="totalFollowers">Total Followers</option>
          <option value="revenue">Revenue</option>
        </select>
        <select v-model="orderDirection" class="form-select">
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
        <select v-model="pageSize" @change="onPageSizeChange" class="form-select">
          <option :value="5">5</option>
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select>
      </div>

      <table class="table table-striped table-bordered table-dark">
        <thead class="table-secondary">
          <tr>
            <th>Creator Name</th>
            <th>Total Followers</th>
            <th>Content Type</th>
            <th>Revenue</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="creator in filteredAndSortedCreators" :key="creator.creatorName">
            <td>{{ creator.creatorName }}</td>
            <td>{{ creator.totalFollowers }}</td>
            <td class="text-uppercase">{{ creator.contentType }}</td>
            <td>{{ creator.revenue.toLocaleString('en-US', { style: 'currency', currency: 'USD' }) }}</td>
          </tr>
        </tbody>
      </table>

      <div class="d-flex justify-content-between align-items-center mt-3">
        <button class="btn btn-secondary" :disabled="currentPage === 1" @click="prevPage">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button class="btn btn-secondary" :disabled="currentPage === totalPages" @click="nextPage">Next</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const loading = ref(false)
const activeTab = ref(localStorage.getItem('activeTab') || 'resume')

function setTab(tab) {
  activeTab.value = tab
  localStorage.setItem('activeTab', tab)
  if (tab === 'other') {
    loadAllCreators()
  } else if (tab === 'resume') {
    fetchContentTypeResume() 
  }
}

const data = ref([])
const searchText = ref('')
const sortOrder = ref('desc')

const sortedAndFiltered = computed(() => {
  let result = data.value.filter(item =>
    item.contentType.toLowerCase().includes(searchText.value.toLowerCase())
  )
  return result.sort((a, b) =>
    sortOrder.value === 'asc'
      ? a.totalFollowers - b.totalFollowers
      : b.totalFollowers - a.totalFollowers
  )
})

async function fetchContentTypeResume() {
  loading.value = true
  const response = await fetch(`${import.meta.env.VITE_API_URL}/content-type-resume`)
  data.value = await response.json()
  loading.value = false
}

const allCreators = ref({ data: [] })
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = ref(5)

const creatorSearchText = ref('')
const orderField = ref('totalFollowers')
const orderDirection = ref('desc')

const filteredAndSortedCreators = computed(() => {
  let result = allCreators.value.data.filter(c =>
    c.creatorName.toLowerCase().includes(creatorSearchText.value.toLowerCase())
  )
  return result.sort((a, b) => {
    const field = orderField.value
    return orderDirection.value === 'asc'
      ? a[field] - b[field]
      : b[field] - a[field]
  })
})

async function loadAllCreators() {
  loading.value = true
  const response = await fetch(`${import.meta.env.VITE_API_URL}/all-creators?page=${currentPage.value}&pageSize=${pageSize.value}`)
  const result = await response.json()
  allCreators.value = result
  totalPages.value = result.totalPages
  loading.value = false
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    loadAllCreators()
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    loadAllCreators()
  }
}

watch(pageSize, () => {
  currentPage.value = 1
  loadAllCreators()
})

onMounted(() => {
  if (activeTab.value === 'resume') {
    fetchContentTypeResume()
  } else {
    loadAllCreators()
  }
})
</script>

<style>
@import 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css';

.custom-background {
  background-color: #1f1f1f;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

.nav-link.active {
  background-color: #0d6efd;
  color: white;
  font-weight: bold;
  border-radius: 6px;
}

.table-dark tbody tr:hover {
  background-color: #2a2a2a;
  cursor: pointer;
}
</style>
