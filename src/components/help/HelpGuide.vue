<script setup lang="ts">
import { PhMouseLeftClick } from '@phosphor-icons/vue'
import {
  DrawingHelp, HelpGuide, HelpSection, ManagingHelp, MeasuresHelp, MenusHelp, NavigationHelp,
} from 'optica-core/ui/help-guide'
</script>

<template>
  <HelpGuide app-name="Stackoptica">
    <template #about>
      <p>Stackoptica shows a focus stack of a specimen: a series of photos (slices), each sharp at a different depth,
        and the images stacked from them, sharp everywhere.</p>
      <p>Placing a landmark on the slice where that point is sharp gives its depth, so measurements are made in 3D.</p>
    </template>

    <NavigationHelp>
      <li>
        <strong>Slider</strong> (in the sidebar): drag it to go through the slices, the counter under the thumbnail
        shows the position of the slice in the stack
      </li>
      <li>
        <kbd class="rounded border px-1 text-xs">↓</kbd> / <kbd class="rounded border px-1 text-xs">↑</kbd>: previous /
        next slice
      </li>
      <li>The buttons above the slider switch between the stack and the stacked images</li>
      <li>
        <PhMouseLeftClick class="inline h-5 w-5 align-text-bottom" weight="fill" /><span
          class="text-xs font-bold">x2</span> on a landmark in the image, or on its position in the sidebar: goes to the
        slice it was placed on
      </li>
    </NavigationHelp>

    <HelpSection title="How it works">
      <li>The slices are sorted from the lowest to the highest, each one is sharp at its own depth</li>
      <li>
        A landmark gets its 3D position <strong>(X; Y; Z)</strong> from the slice it is placed on:
        <ul class="mt-1 list-[circle] pl-5 space-y-1">
          <li><strong>X</strong> and <strong>Y</strong>: the pixel position, scaled by the pixel spacing of the slice</li>
          <li><strong>Z</strong>: the depth of the slice</li>
        </ul>
      </li>
      <li>
        Annotations are placed on the slices only: the stacked images can be looked at, not annotated
      </li>
      <li>
        A landmark is shown on every slice. Moving it on another slice gives it the depth of that slice
      </li>
      <li>
        The landmarks of a distance or polygon can be on different slices, a box stays on the slice of its first
        corner
      </li>
    </HelpSection>

    <DrawingHelp />

    <ManagingHelp />

    <MeasuresHelp>
      <template #intro>
        <li>All values are in 3D: they include the depth of the slices</li>
      </template>
    </MeasuresHelp>

    <MenusHelp />
  </HelpGuide>
</template>
