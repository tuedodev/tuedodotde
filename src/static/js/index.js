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
		_resizeObserver();
		_deleteNotifications();
		if (typeof hljs !== `undefined`) {
			hljs.initHighlightingOnLoad();
		}
		if (typeof AOS !== `undefined`) {
			_blogpostAddAnimation();
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
		let video = document.querySelector(`video.background-video`);
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
		if (video) {
			video.playbackRate = 0.75;
		}
	};

	const _resizeObserver = () => {
		const BREAKPOINT = 1025;
		const videoElement = document.querySelector('.background-video');
		if (videoElement) {
			let src1 = document.createElement('source');
			let src2 = document.createElement('source');
			let src3 = document.createElement('source');
			src1.setAttribute('src', videoElement.dataset.source1);
			src1.setAttribute('type', videoElement.dataset.type1);
			src2.setAttribute('src', videoElement.dataset.source2);
			src2.setAttribute('type', videoElement.dataset.type2);
			src3.setAttribute('src', videoElement.dataset.source3);
			src3.setAttribute('type', videoElement.dataset.type3);
			videoElement.appendChild(src1);
			videoElement.appendChild(src2);
			videoElement.appendChild(src3);
			videoElement.playbackRate = 0.9;
			videoElement.setAttribute('muted', '');
			const body = document.querySelector('body');
			let playPromise;

			const resizeObserver = new ResizeObserver((entries) => {
				for (let entry of entries) {
					let vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
					if (videoElement) {
						if (vw >= BREAKPOINT) {
							// Videos on Desktop only
							videoElement.setAttribute('autoplay', '');
							playPromise = videoElement.play();
						} else {
							// Deactivate videos for mobile
							videoElement.removeAttribute('autoplay');
							if (playPromise !== undefined) {
								playPromise
									.then((_) => {
										videoElement.pause();
									})
									.catch((error) => {});
							}
						}
					}
				}
			});
			resizeObserver.observe(body);
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

	const _blogpostAddAnimation = () => {
		let blogContent = document.querySelector(`.blog-content`);
		if (blogContent) {
			let headers = Array.prototype.slice.call(blogContent.querySelectorAll(`h2`, `h3`, `h4`, `h5`, `h6`), 0);
			headers.forEach((header) => {
				header.setAttribute(`data-aos`, `fade-left`);
			});
		}
	};

	_init();
});
