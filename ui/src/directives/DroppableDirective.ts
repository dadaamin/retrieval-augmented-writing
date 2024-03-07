// src/directives/DroppableDirective.ts

import { DirectiveBinding, ObjectDirective } from "vue";

const DroppableDirective: ObjectDirective<HTMLElement> = {
    mounted(el: HTMLElement, binding: DirectiveBinding, vnode) {
        el.addEventListener("dragover", (e: DragEvent) => {
            e.preventDefault(); // Necessary to allow dropping
            el.style.opacity = "0.7"; // Visual feedback
        });

        el.addEventListener("dragleave", () => {
            el.style.opacity = "1"; // Revert visual feedback
        });

        el.addEventListener("drop", (e: DragEvent) => {
            e.preventDefault();
            el.style.opacity = "1"; // Revert visual feedback

            // Emit an event to the parent component
            vnode.el.dispatchEvent(
                new CustomEvent("item-dropped", {
                    detail: { droppedItem: e.dataTransfer?.getData("text") }, // Using optional chaining
                    bubbles: true,
                })
            );
        });
    },
};

export default DroppableDirective;
