<script setup lang="ts">
import { downloadCSV, downloadJSON, exportFilename } from '@optica/core'
import { AppMenu } from '@optica/core/ui/app-menu'
import { useImagesStore, useSettingsStore } from '@/lib/stores'
import { Credits } from '@/components/credits'

const settingsStore = useSettingsStore()
const imagesStore = useImagesStore()

// the annotations of every acquisition, by acquisition id
function exportAnnotations(format: "csv" | "json") {
  const project = imagesStore.project
  if (!project) {
    return
  }
  if (format == "csv") {
    downloadCSV(project.annotationsToCSVRows(), exportFilename("stack", imagesStore.objectPath, "csv"))
  } else {
    downloadJSON(project.annotationsToJSON(), exportFilename("stack", imagesStore.objectPath, "json"))
  }
}

// also reads the files exported by the old Stackoptica (one set of annotations)
function importAnnotations(content: string) {
  imagesStore.project?.importAnnotations(JSON.parse(content))
}
</script>

<template>
  <AppMenu :reverse="settingsStore.isLeft" @update:reverse="settingsStore.useToggleLeft" app-name="Stackoptica"
    @export="exportAnnotations" @import="importAnnotations">
    <template #credits>
      <Credits />
    </template>
  </AppMenu>
</template>
