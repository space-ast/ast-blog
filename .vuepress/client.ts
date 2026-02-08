import { defineClientConfig } from "vuepress/client";
import { setupTransparentNavbar } from "vuepress-theme-hope/presets/transparentNavbar.js";
// 将博主信息移动至文章列表的左侧
import "vuepress-theme-hope/presets/left-blog-info.scss"

export default defineClientConfig({
  setup: () => {
    setupTransparentNavbar({ type: "homepage" });
  },
});