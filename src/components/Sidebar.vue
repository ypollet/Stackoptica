<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { AnnotationsPanel } from 'optica-core/ui/annotations-panel'
import { Label } from 'optica-core/ui/label'
import { Slider } from 'optica-core/ui/slider'
import { ImageOverview } from 'optica-core/ui/image-overview'
import { ToggleImage } from 'optica-core/ui/toggle-image'
import { useImagesStore } from '@/lib/stores'
import { vectorToString } from 'optica-core'

const imagesStore = useImagesStore()
const { acquisition, annotations, selectedImage } = storeToRefs(imagesStore)

const STACK = "stack"

const images = computed(() => [
  { value: STACK, label: "Stack" },
  ...(acquisition.value?.standaloneImages ?? []).map((stacked) => ({ value: stacked.name, label: stacked.label })),
])

function selectImage(value: string | undefined) {
  if (value != undefined) {
    imagesStore.selectStacked(value == STACK ? null : value)
  }
}
</script>

<template>
  <div class="flex flex-col pb-[12px] w-auto h-full">
    <!-- shown image, and its slice while on the stack -->
    <ImageOverview v-if="acquisition && selectedImage" :image="selectedImage" :size="acquisition.sizeOf()"
      :camera="acquisition.camera" :counter="imagesStore.onStack ? `${acquisition.index + 1}/${acquisition.images.length}` : undefined" />
    <!-- the stack or one of the images stacked from it -->
    <ToggleImage v-if="acquisition" :items="images" :model-value="acquisition.standalone ?? STACK"
      @update:model-value="selectImage" />
    <div class="flex-none space-y-4 py-4">
      <div v-if="acquisition && acquisition.hasGroup" class="px-3 py-2">
        <Slider :model-value="[acquisition.index]" :max="acquisition.images.length - 1" :step="1"
          @update:model-value="(value) => { if (value) imagesStore.setIndex(value[0]!) }" />
        <div class="mt-1.5 flex flex-row justify-between">
          <span v-for="image in acquisition.images" :key="image.name" class="w-5 text-center">|</span>
        </div>
      </div>
      <!-- the annotations of the stack -->
      <AnnotationsPanel v-if="annotations" :annotations="annotations"
        @activate="(landmark) => acquisition?.select(landmark.pose.image.name)">
        <template #landmark-info="{ landmark }">
          <Label class="whitespace-nowrap" title="Double click: go to its image"
            @dblclick.stop="acquisition?.select(landmark.pose.image.name)">
            {{ vectorToString(landmark.position) }}
          </Label>
        </template>
        <!-- a box is on one image: double click goes to it -->
        <template #measure-info="{ annotation }">
          <Label v-if="annotations.onOneImage(annotation) && annotations.imageOf(annotation)" class="whitespace-nowrap"
            title="Image on which all the landmarks are placed" @dblclick.stop="acquisition?.select(annotations.imageOf(annotation)!.name)">
            {{ annotations.imageOf(annotation)!.label }}
          </Label>
        </template>
        <template #measure-landmark-info="{ landmark }">
          <Label class="whitespace-nowrap" title="Double click: go to its image"
            @dblclick.stop="acquisition?.select(landmark.pose.image.name)">
            {{ vectorToString(landmark.position) }}
          </Label>
        </template>
      </AnnotationsPanel>
    </div>
  </div>
</template>
