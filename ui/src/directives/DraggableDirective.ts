// src/directives/DraggableDirective.ts

import { DirectiveBinding, ObjectDirective } from "vue";

const DraggableDirective: ObjectDirective<HTMLElement> = {
    mounted(el: HTMLElement) {
        el.style.cursor = "grab";

        el.onmousedown = function (e: MouseEvent) {
            const offsetX = e.clientX - el.getBoundingClientRect().left;
            const offsetY = e.clientY - el.getBoundingClientRect().top;

            function moveAt(pageX: number, pageY: number) {
                el.style.position = "absolute"; // Ensure the element is positioned absolutely
                el.style.left = pageX - offsetX + "px";
                el.style.top = pageY - offsetY + "px";
            }

            function onMouseMove(event: MouseEvent) {
                moveAt(event.pageX, event.pageY);
            }

            document.addEventListener("mousemove", onMouseMove);

            el.onmouseup = function () {
                document.removeEventListener("mousemove", onMouseMove);
                el.onmouseup = null;
            };
        };

        el.ondragstart = function () {
            return false;
        };
    },
};

export default DraggableDirective;
