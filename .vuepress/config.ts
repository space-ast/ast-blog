import { defineUserConfig } from "vuepress";

import theme from "./theme.js";

export default defineUserConfig({
  base: "/ast-blog/",

  lang: "zh-CN",
  title: "ast-blog",
  description: "a blog about astronomy and astrodynamics",

  theme,

  // 和 PWA 一起启用
  // shouldPrefetch: false,
});
