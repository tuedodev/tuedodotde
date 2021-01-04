import { makeAjaxRequest } from './ajax.js';
import { addHTMLtoElement, clearHTMLElement, animateElement } from './utils.js';
import { disableScroll, enableScroll } from './noscrolling.js';
import Captcha from './Captcha.js';
import FormApp from './FormApp.js';

export default class Modal {
	
	constructor({ baseForm, html, captcha = null, redirectURL = null }) {
		let modal = document.querySelector(`.modal`);
		this.modal = modal;
		this.baseForm = baseForm;
		this.html = html;
		this.redirectURL = redirectURL;
		this.captcha = captcha;
		this.captchaImageID = null;
		this.modalForm = null;
		this.iconReloadButton = null;
	}

	updateModalwithHtml = () => {
		if (this.modal !== null) {
			clearHTMLElement(this.modal);
			addHTMLtoElement({
				element: this.modal,
				kidClass: ``,
				html: this.html,
			});
			this.modalForm = this.modal.querySelector(`.modal form`);
			if (this.captcha !== null) {
				this.captchaImageID = document.getElementById(`captcha-image`);
				this.updateCaptcha();
				this.iconReloadButton = document.getElementById('icon_reload_button');
				if (this.iconReloadButton !== null) {
					this.iconReloadButton.addEventListener('click', (event) => {
						this.iconReloadButtonHandler();
					});
				}
			}
		}
	};

	updateCaptcha = async () => {
		await this.captcha.update();
		if (this.captcha.captchaImage !== null) {
			clearHTMLElement(this.captchaImageID);
			this.captchaImageID.appendChild(this.captcha.captchaImage);
		}
	};

	registerModalEventListeners = ({ resolve, reject }) => {
		let deleteBtn = this.modal.querySelector(`.modal-delete`);

		if (this.modalForm) {
			this.modalForm.addEventListener(`submit`, (event) => {
				event.preventDefault();
				this.handleModalSubmitButton({ resolve, reject });
			});
		}
		deleteBtn.addEventListener(`click`, (event) => {
			reject({ modal: this, errMsg: `Modal closed from deleteBtn` });
		});
		window.addEventListener(`click`, (event) => {
			let evt = event || window.event;
			if (evt.target && evt.target.classList.contains(`modal-background`)) {
				reject({ modal: this, errMsg: `Modal closed from outside window click` });
			}
		});
	};

	captchaConfirmation = () => {
		return new Promise((resolve, reject) => {
			if (this.modal) {
				this.captcha = new Captcha(this);
				this.updateModalwithHtml();
				this.openModal();
				this.captcha.captchaForm = new FormApp(`captcha`);
				this.captcha.captchaForm.init();
				this.registerModalEventListeners({ resolve, reject });
				this.captcha.captchaForm.submitButton.addEventListener(`click`, async (event) => {
					this.handleModalSubmitButton({ resolve, reject });
				});
			} else {
				reject({ modal: this, errorMsg: `Ein Fehler ist aufgetreten.` });
			}
		});
	};

	messageConfirmation = () => {
		return new Promise((resolve) => {
			if (this.modal) {
				this.updateModalwithHtml();
				this.openModal();
				let deleteBtn = this.modal.querySelector(`.modal-delete`);
				let submitBtn = this.modal.querySelector(`.modal .control .button`);
				submitBtn.addEventListener(`click`, (event) => {
					resolve({ modal: this });
				});
				deleteBtn.addEventListener(`click`, (event) => {
					resolve({ modal: this });
				});
				window.addEventListener(`click`, (event) => {
					let evt = event || window.event;
					if (evt.target && evt.target.classList.contains(`modal-background`)) {
						resolve({ modal: this });
					}
				});
			} else {
				reject({ modal: this, errorMsg: `Ein Fehler ist aufgetreten.` });
			}
		});
	};

	handleModalSubmitButton = async ({ resolve, reject }) => {
		if (this.baseForm && this.captcha) {
			let baseForm = this.baseForm;
			let captchaForm = this.captcha.captchaForm;
			let data = await captchaForm.validateFormOnServer(captchaForm);
			if (!data.hasOwnProperty(`errors`)) {
				let body = baseForm.constructBodyObject();
				let site_path_elem = document.querySelector('form #site_path');
				let site_path = site_path_elem ? site_path_elem.value : '';
				let captchaObj = {
					captcha_input: this.captcha.captchaForm.fields[0].input.value,
					action: this.baseForm.formHandler,
					site_path: site_path,
				};
				body = { ...captchaObj, ...body };
				let obj = { body, url: '/process_form/', csrftoken: baseForm.csrftoken };
				let data = await makeAjaxRequest(obj);
				let html = '';
				if (!data.error_html) {
					html = data.message_html;
				} else {
					html = data.error_html;
				}
				this.redirectURL = data.redirect_url;
				resolve({
					modal: this,
					html: html,
					redirectURL: data.redirect_url,
				});
			}
		}
	};

	openModal = () => {
		if (this.modal !== null) {
			let classList = this.modal.classList;
			if (!classList.contains(`is-active`)) {
				classList.add(`is-active`);
				classList.add(`open`);
				disableScroll();
			}
		}
	};

	closeModal = (redirectURL = null) => {
		return new Promise((resolve) => {
			let classList = this.modal.classList;
			enableScroll();
			classList.remove(`open`);
			animateElement({
				element: this.modal,
				cssClass: `close`,
				callback: function () {
					classList.remove(`is-active`);
					classList.remove(`close`);
					if (redirectURL !== null) {
						window.location.replace(redirectURL);
					}
					resolve({});
				},
				milliseconds: 200,
			});
		});
	};

	iconReloadButtonHandler = (event) => {
		if (this.iconReloadButton !== null && !this.iconReloadButton.classList.contains(`is-loading`)) {
			this.iconReloadButton.classList.add(`is-loading`);
			this.updateCaptcha().then(() => {
				this.iconReloadButton.classList.remove(`is-loading`);
			});
		}
	};
}
