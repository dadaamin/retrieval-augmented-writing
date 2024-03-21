import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import AppLayout from "@/layout/AppLayout.vue";

const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        component: AppLayout,
        children: [
            {
                path: "/",
                redirect:
                    "/mtb-protocol?patient=5ab37373015afdba99481e774141ddee2346e891e8c4d8444f17c3d2d38d7d74",
            },
            {
                path: "/mtb-protocol",
                // route level code-splitting
                // this generates a separate chunk (about.[hash].js) for this route
                // which is lazy-loaded when the route is visited.
                component: () =>
                    import(
                        /* webpackChunkName: "about" */ "../layout/TumorBoardDocumentation/Layout.vue"
                    ),
            },
            {
                path: "/about",
                name: "about",
                // route level code-splitting
                // this generates a separate chunk (about.[hash].js) for this route
                // which is lazy-loaded when the route is visited.
                component: () =>
                    import(
                        /* webpackChunkName: "about" */ "../views/AboutView.vue"
                    ),
            },
        ],
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
