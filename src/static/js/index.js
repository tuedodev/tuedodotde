import AOS from 'aos';
try {
	require('../scss/main.scss');
} catch (err) {
	console.log('New Sass File NOT compiled.');
}
import FormApp from './FormApp.js';

function ready(fn) {
	if (document.readyState != 'loading') {
		fn();
	} else {
		document.addEventListener('DOMContentLoaded', fn);
	}
}

ready(() => {
	const _init = () => {
		_toggleNavigation();
		FormApp._initForms(['comment', 'contact', 'subscribe']);
		let navbar = document.querySelector(`.navbar`);
		window.addEventListener('scroll', _shrinkNavigation.bind(null, navbar));
		_adjustLayout();
		_footerObserver();
		_deleteNotifications();
		if (typeof hljs !== `undefined`) {
			hljs.initHighlightingOnLoad();
		}
		if (typeof AOS !== `undefined`) {
			AOS.init();
		}
	};

	const _toggleNavigation = () => {
		// Get all "navbar-burger" elements
		const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

		// Check if there are any navbar burgers
		if ($navbarBurgers.length > 0) {
			// Add a click event on each of them
			$navbarBurgers.forEach((el) => {
				el.addEventListener('click', () => {
					// Get the target from the "data-target" attribute
					const target = el.dataset.target;
					const $target = document.getElementById(target);

					// Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
					el.classList.toggle('is-active');
					$target.classList.toggle('is-active');
				});
			});
		}
	};

	const _shrinkNavigation = (element) => {
		if (window.pageYOffset > 100) {
			element.classList.remove(`is-spaced`);
		} else {
			if (!element.classList.contains(`is-spaced`)) {
				element.classList.add(`is-spaced`);
			}
		}
	};

	const _footerObserver = () => {
		let element = document.getElementById('main-footer');
		let options = {
			root: null,
			rootMargin: '0px',
			threshold: [0.3, 0.6],
		};
		let observer = new IntersectionObserver(_displayFooter, options);
		observer.observe(element);
	};

	const _displayFooter = (entries) => {
		entries.forEach((entry) => {
			if (entry.isIntersecting && entry.intersectionRatio > 0.6) {
				let classList = entry.target.classList;
				if (!classList.contains(`footer-show`)) {
					classList.add(`footer-show`);
				}
			} else {
				let classList = entry.target.classList;
				classList.remove(`footer-show`);
			}
		});
	};

	const _adjustLayout = () => {
		let headers = document.querySelectorAll(`.tuedo-header`);
		let background = document.querySelectorAll(`.tuedo-header__background-text`);
		headers.forEach((x) => {
			let le = x.textContent.length;
			x.style.fontSize = `${_calculateFontSize(le)}rem`;
		});
		if (background) {
			background.forEach((x) => {
				let le = x.textContent.length;
				x.style.fontSize = `${_calculateFontSize(le) * 2}rem`;
			});
		}
	};

	const _calculateFontSize = (le) => {
		if (le > 15) {
			le = 15;
		} else if (le < 5) {
			le = 5;
		}
		return 3.6 - (le - 5) * 0.2;
	};

	const _deleteNotifications = () => {
		let notifications = document.querySelectorAll('.notification .delete') || [];
		notifications.forEach((x) => {
			let notification = x.parentNode;
			x.addEventListener('click', () => {
				notification.parentNode.removeChild(notification);
			});
		});
	};
	
	_init();
});
