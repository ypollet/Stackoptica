import { defineStore } from 'pinia'
import type { Project, ProjectImage } from 'optica-core'
import { getRepository } from '@/data/setup'

export const useSettingsStore = defineStore('settings', {
  state: () => ({ isLeft: false }),
  actions: {
    useToggleLeft(value: boolean) {
      this.isLeft = value
    },
  },
  persist: {
    storage: localStorage,
    key: 'settings',
  }
})

// The project holds everything else: images, camera and annotations of the stack.
// Its annotations are saved by usePersistedAnnotations (ViewerView).
export const useImagesStore = defineStore('images', {
  state: () => ({
    objectPath: "",
    project: null as Project<ProjectImage> | null,
  }),
  getters: {
    acquisition: (state) => state.project?.acquisition ?? null,
    annotations: (state) => state.project?.acquisition?.annotations ?? null,
    selectedImage(): ProjectImage | null {
      return this.acquisition?.selectedImage ?? null
    },
    // landmarks are placed on the slices only: the stacked images have no position
    onStack(): boolean {
      return this.acquisition != null && this.acquisition.standalone == null
    },
  },
  actions: {
    setPath(path: string) {
      this.$reset()
      this.objectPath = path
    },
    // computes the positions that aren't known: old exports have none, a reload during a computation loses one
    recomputePositions() {
      const repository = getRepository()
      this.project?.acquisitions.forEach((acquisition) => {
        acquisition.annotations.recomputePositions((pose) => repository.computeLandmarkPosition(this.objectPath, pose))
      })
    },
    setIndex(index: number) {
      this.acquisition?.setIndex(index)
    },
    increment() {
      this.acquisition?.moveIndex(1)
    },
    decrement() {
      this.acquisition?.moveIndex(-1)
    },
    // null goes back to the stack
    selectStacked(name: string | null) {
      this.acquisition?.selectStandalone(name)
    },
  },
})
