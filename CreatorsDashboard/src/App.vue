
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
        <thead class="table-secondary">
          <tr>
            <th>Content Type</th>
            <th>Total Followers</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in sortedAndFiltered" :key="item.contentType">
            <td>{{ item.contentType }}</td>
            <td>{{ item.totalFollowers }}</td>
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
import { ref, computed, onMounted } from 'vue'

const activeTab = ref('resume')
function setTab(tab) {
  activeTab.value = tab
  if (tab === 'other') loadAllCreators()
}

const data = ref([])
const searchText = ref('')
const sortOrder = ref('desc')

const sortedAndFiltered = computed(() => {
  let result = data.value.filter(item =>
    item.contentType.toLowerCase().includes(searchText.value.toLowerCase())
  )

  result = result.sort((a, b) => {
    if (sortOrder.value === 'asc') {
      return a.totalFollowers - b.totalFollowers
    } else {
      return b.totalFollowers - a.totalFollowers
    }
  })

  return result
})

async function fetchContentTypeResume() {
  const response = await fetch('http://localhost:3000/content-type-resume')
  data.value = await response.json()
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

  result = result.sort((a, b) => {
    const field = orderField.value
    if (orderDirection.value === 'asc') {
      return a[field] - b[field]
    } else {
      return b[field] - a[field]
    }
  })

  return result
})

async function loadAllCreators() {
  const response = await fetch(`http://localhost:3000/all-creators?page=${currentPage.value}&pageSize=${pageSize.value}`)
  const result = await response.json()
  allCreators.value = result
  totalPages.value = result.totalPages
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

function onPageSizeChange() {
  currentPage.value = 1
  loadAllCreators()
}

onMounted(() => {
  fetchContentTypeResume()
})
</script>

<style>
@import 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css';

.custom-background {
  background-color: #2f2f2f;
  padding: 20px;
  border-radius: 8px;
}

.nav-link.active {
  background-color: #444;
  color: #fff;
}
</style>
