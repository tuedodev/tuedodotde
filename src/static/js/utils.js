export const addHTMLtoElement = (obj) => {
	let kid = document.createElement('div');
	obj.kidClass.split(' ').forEach((x) => {
		if (x.length > 0) {
			kid.classList.add(x);
		}
	});
	kid.innerHTML = obj.html;
	obj.element.prepend(kid);
};

export const clearHTMLElement = (element) => {
	while (element.firstChild) {
		element.removeChild(element.lastChild);
	}
};

export const animateElement = ({ element, cssClass, callback, milliseconds }) => {
	if (!element.classList.contains(cssClass)) {
		element.classList.add(cssClass);
		setTimeout(callback, milliseconds);
	}
};
