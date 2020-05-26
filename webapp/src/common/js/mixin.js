import { dateFtt } from './utils'

export const dataMixin = {
  data () {
    return {
      tableData: [],
      multipleSelection: [],
      showDialog: false,
      dialogTitle: '',
      totalNumbers: 0
    }
  },
  methods: {
    handleSelectionChange (val) {
      const selectData = val.map(item => item.id)
      this.multipleSelection = selectData
    },
    handleDelete () {
      if (this.multipleSelection.length < 1) {
        this.$message.error('Select at least one item')
        return
      }
      this.$messageBox.confirm('Confirm?', 'Notify', {
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
        type: 'warning'
      }).then(() => {
        this.deletePageData && this.deletePageData()
      }).catch(() => {
        this.$message({
          type: 'info',
          message: 'Cancle'
        })
      })
    },
    handleCurrentChange (currentPage) {
      this.searchForm.pageIndex = currentPage
      this.getPageData && this.getPageData()
    },
    handleSearch () {
      this.searchForm.pageIndex = 1
      this.getPageData && this.getPageData()
    },
    handleCancel () {
      Object.keys(this.searchForm).forEach(key => {
        if (key === 'pageIndex') {
          this.searchForm[key] = 1
        } else {
          this.searchForm[key] = ''
        }
      })
      this.getPageData && this.getPageData()
    },
    dialogClosed () {
      if (this.formData.id) {
        delete this.formData.id
      }
      Object.keys(this.formData).forEach(key => {
        this.formData[key] = ''
      })
    },
    toggleDialog () {
      this.showDialog = !this.showDialog
    },
    indexMethod (index) {
      return (this.searchForm.pageIndex - 1) * 10 + index + 1
    },
    formatTime (time) {
      return dateFtt('yyyy-MM-dd hh:ss:mm', new Date(time))
    },
    setFormData (data) {
      Object.keys(this.formData).forEach(key => {
        this.formData[key] = data[key] || ''
      })
      this.formData.id = data.id
    }
  }
}
