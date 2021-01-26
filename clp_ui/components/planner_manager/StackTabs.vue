<template>
  <v-card color="#E5E7EB" class="h-full" style="position: relative">
    <v-tabs v-model="tab" background-color="#E5E7EB">
      <v-tab href="#tab-1">
        Recents
      </v-tab>

      <v-tab href="#tab-2">
        Favorites
      </v-tab>
    </v-tabs>

    <v-tabs-items
      v-model="tab"
      class="overflow-y-auto"
      style="height:80%; background-color:#E5E7EB"
    >
      <v-tab-item
        v-for="i in 3"
        :key="i"
        :value="'tab-' + i"
        class="bg-gray-200"
      >
        <!-- <v-card flat>
          <v-card-text
            >Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet
            harum deleniti libero ab labore cum laboriosam impedit praesentium
            nobis non saepe veritatis, quidem molestiae a ut ex unde architecto
            voluptate.</v-card-text
          >
        </v-card> -->
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>
import box from "@/mixins/box";
export default {
  mixins: [box],
  data: () => ({
    tab: 0
  })
};
</script>
