<template>
  <note-pdf :data="notePdfData"></note-pdf>
</template>

<script setup lang="ts">
  import notePdf from "../element/widgets/notepdf.vue"

  const notePdfData = {
    pdf_file: 'https://arxiv.org/pdf/2403.14740',
    notes: [
      {page: 1, x: 100, y: 100, text: "毕导：为什么开水和凉水听起来不一样"}
    ]
  }
</script>