<template>
  <div class="report-viewer" v-html="renderedHtml"></div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'

const props = defineProps<{
  content: string
}>()

const md = new MarkdownIt({
  highlight: function (str: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (_) {}
    }
    return ''
  },
})

const renderedHtml = computed(() => md.render(props.content || ''))
</script>

<style scoped>
.report-viewer {
  padding: 20px;
  line-height: 1.8;
}
.report-viewer :deep(h1) { font-size: 24px; margin-bottom: 16px; }
.report-viewer :deep(h2) { font-size: 20px; margin: 24px 0 12px; }
.report-viewer :deep(h3) { font-size: 16px; margin: 20px 0 10px; }
.report-viewer :deep(blockquote) {
  border-left: 4px solid #409eff;
  padding-left: 16px;
  color: #606266;
  margin: 16px 0;
}
.report-viewer :deep(pre) {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 4px;
  overflow-x: auto;
}
.report-viewer :deep(table) {
  border-collapse: collapse;
  width: 100%;
}
.report-viewer :deep(th), .report-viewer :deep(td) {
  border: 1px solid #ebeef5;
  padding: 8px 12px;
}
.report-viewer :deep(th) { background: #f5f7fa; }
</style>
