// Source: https://stackoverflow.com/questions/4770025/how-to-disable-scrolling-temporarily/21533631#21533631
// with some modifications for modules and exporting
// left: 37, up: 38, right: 39, down: 40,
// spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36

function scrollPreventDefault(e) {
	e.preventDefault();
}

function preventDefaultForScrollKeys(e) {
	let keys = { 37: 1, 38: 1, 39: 1, 40: 1 };
	if (keys[e.keyCode]) {
		scrollPreventDefault(e);
		return false;
	}
}

function getScrollParam() {
	// modern Chrome requires { passive: false } when adding event
	let supportsPassive = false;
	try {
		window.addEventListener(
			'test',
			null,
			Object.defineProperty({}, 'passive', {
				get: function () {
					supportsPassive = true;
				},
			})
		);
	} catch (e) {}
	let wheelOpt = supportsPassive ? { passive: false } : false;
	let wheelEvent = 'onwheel' in document.createElement('div') ? 'wheel' : 'mousewheel';
	return {
		supportsPassive: supportsPassive,
		wheelOpt: wheelOpt,
		wheelEvent: wheelEvent,
	};
}

// call this to Disable
export function disableScroll() {
	let scrollParam = getScrollParam();
	window.addEventListener('DOMMouseScroll', scrollPreventDefault, false); // older FF
	window.addEventListener(scrollParam.wheelEvent, scrollPreventDefault, scrollParam.wheelOpt); // modern desktop
	window.addEventListener('touchmove', scrollPreventDefault, scrollParam.wheelOpt); // mobile
	window.addEventListener('keydown', preventDefaultForScrollKeys, false);
}

// call this to Enable
export function enableScroll() {
	let scrollParam = getScrollParam();
	window.removeEventListener('DOMMouseScroll', scrollPreventDefault, false);
	window.removeEventListener(scrollParam.wheelEvent, scrollPreventDefault, scrollParam.wheelOpt);
	window.removeEventListener('touchmove', scrollPreventDefault, scrollParam.wheelOpt);
	window.removeEventListener('keydown', preventDefaultForScrollKeys, false);
}
