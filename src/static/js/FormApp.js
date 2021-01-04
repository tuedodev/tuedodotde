import { makeAjaxRequest } from './ajax.js';
import { getCSRFToken } from './csrftoken.js';
import Modal from './Modal.js';
import { animateElement } from './utils.js';

export default class FormApp {
	
	static defaultValidationMessage = 'Fehler bei der Eingabe.';
	
	static validationFuncs = {
		required: function (field) {
			let input = FormApp.getValueFromInput(field);
			let errMsg = this.errorMsg['error_msg_required'] || FormApp.defaultValidationMessage;
			let valid = field.isCheckbox ? input : input.length > 0;
			return { valid: valid, error_msg: valid === true ? '' : errMsg };
		},
		email: function (field) {
			let input = FormApp.getValueFromInput(field);
			let valid = true;
			let errMsg = this.errorMsg['error_msg_email_invalid'] || FormApp.defaultValidationMessage;
			if (input.length > 0) {
				const email_regex = new RegExp('^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,6}$', 'g');
				valid = email_regex.test(input);
			}
			return { valid: valid, error_msg: valid === true ? '' : errMsg };
		},
	};

	static getValueFromInput(field, trim = true) {
		let input = field.input.value;
		if (field.isCheckbox) {
			input = field.input.checked;
		} else {
			input = trim ? input.trim() : input;
		}
		return input;
	}
	
	constructor(className) {
		this.className = className;
		this.form = document.querySelector(`.${className}`);
		if (this.form !== null) {
			this.submitButton = this.form.querySelector(`.control > .button`);
			this.csrftoken = getCSRFToken('csrftoken');
			let fields = Array.prototype.slice.call(this.form.querySelectorAll(`.field`), 0);
			let fields_filtered = fields.filter(
				(x) =>
					x.querySelector(`input:not([disabled]):not([type="submit"]), textarea:not([disabled])`) !== null
			);
			this.fields = Array.prototype.slice.call(fields_filtered, 0);
			let _errorMsg = {};
			const _dataset = this.form.dataset;
			const _dataset_obj = JSON.parse(JSON.stringify(_dataset));
			for (const [key, value] of Object.entries(_dataset_obj)) {
				Object.defineProperty(_errorMsg, key, { value });
			}
			this.errorMsg = _errorMsg;
			this.fields = this.fields.map(function (x) {
				let isGrouped = x.classList.contains(`is-grouped`);
				let parent = x;
				if (isGrouped) {
					parent = x.parentElement;
				}
				let input = x.querySelector(`input, textarea`);
				let name = input.name;
				let id = input.id;
				let inputRect = input.getBoundingClientRect();
				let parentRect = parent.getBoundingClientRect();
				let labelProxy = parent.querySelector(`.labelProxy`);
				let field__label = parent.querySelector(`.field__label`);
				let field__labelRect = field__label !== null ? field__label.getBoundingClientRect() : null;
				let field__help__msg = parent.querySelector(`.field__help__msg`);
				let isTextarea = x.querySelector(`textarea`) !== null ? true : false;
				let checkbox = x.querySelector(`input[type=checkbox]`);
				let isCheckbox = checkbox !== null ? true : false;
				if (isCheckbox) {
					checkbox = checkbox.parentElement;
				}
				let isCaptcha = className === `captcha`;
				let validation = x.dataset.validation;
				let validationFunctions = [];
				let validators = [];
				if (validation !== undefined && validation.length > 0) {
					let validationArray = validation.split(' ');
					validators = validationArray.filter((validator) =>
						FormApp.validationFuncs.hasOwnProperty(validator)
					);
					validationFunctions = validators.map((x) => FormApp.validationFuncs[x]);
				}

				return {
					id,
					name,
					parent: x,
					parentRect,
					input,
					inputRect,
					labelProxy,
					field__label,
					field__labelRect,
					field__help__msg,
					checkbox,
					isTextarea,
					isCheckbox,
					isCaptcha,
					validators,
					validationFunctions,
				};
			});
			this.labelProxyFontSize =
				parseInt(
					window
						.getComputedStyle(document.querySelector(`.${className} .labelProxy`))
						.getPropertyValue('font-size'),
					10
				) || 24;
			let fields_array = this.fields.filter((x) => !x.isCheckbox);
			this.standardInputHeight =
				Math.min(...Array.prototype.map.call(fields_array, (x) => x.inputRect.height)) || 40;
			this.formHandler = className !== `captcha` ? `process_${className}` : null;
			this.redirectURL = null;
			this.captchaForm = null;
		} else {
			return { invalid: true };
		}
	}

	init = () => {
		// Check first time only when field is actually filled
		this.fields
			.filter((x) => FormApp.getValueFromInput(x).length > 0)
			.forEach((x) => this.adjustErrorLabel(x));
		this.adjustLabels();
		this.registerEventListeners();
	};

	getPositionsFromField = (field) => {
		return {
			focused: {
				x: 0,
				y: `${field.field__labelRect.top - field.parentRect.top}px`,
			},
			not_focused: {
				x: `calc(0.60em - 2px)`,
				y: `${
					field.inputRect.top -
					field.parentRect.top +
					this.standardInputHeight / 2 -
					this.labelProxyFontSize / 2
				}px`,
			},
		};
	};

	adjustLabels = () => {
		this.fields.forEach((x) => {
			if (!x.isCheckbox && x.labelProxy !== null) {
				this.checkIfFieldIsFilled(x);
				let positions = this.getPositionsFromField(x);
				let parentClassList = x.parent.classList;
				if (parentClassList.contains(`field--focused`) || parentClassList.contains(`field--notempty`)) {
					x.labelProxy.style.top = positions.focused.y;
					x.labelProxy.style.left = positions.focused.x;
				} else {
					x.labelProxy.style.top = positions.not_focused.y;
					x.labelProxy.style.left = positions.not_focused.x;
				}
			}
		});
	};

	adjustErrorLabel = (field) => {
		let result = this.validateField(field);
		if (!result.valid) {
			this.displayErrorInField({
				field: field,
				errorMsg: result.errorMsg,
			});
		} else {
			if (!field.isCaptcha) {
				this.removeErrorInField(field);
			}
		}
	};

	validateField = (field) => {
		if (field.validationFunctions.length > 0) {
			let arr = field.validationFunctions.map((func) => func.call(this, field));
			arr = arr.filter((x) => !x.valid);
			if (arr.length > 0) {
				let error = arr[0];
				return {
					valid: false,
					errorMsg: error.error_msg,
				};
			} else {
				return {
					valid: true,
					errorMsg: '',
				};
			}
		} else {
			return {
				valid: true,
				errorMsg: '',
			};
		}
	};

	displayErrorInField = ({ field, errorMsg }) => {
		let classList = field.parent.classList;
		let field__help__msg = field.field__help__msg;
		field__help__msg.textContent = errorMsg;
		classList.remove(`field--success`);
		classList.add(`field--warning`);
		if (!field__help__msg.classList.contains(`slideIn`)) {
			animateElement({
				element: field__help__msg,
				cssClass: `slideIn`,
				callback: function () {},
				milliseconds: 200,
			});
		}
	};

	removeErrorInField = (field) => {
		let classList = field.parent.classList;
		let field__help__msg = field.field__help__msg;
		classList.remove(`field--warning`);
		classList.add(`field--success`);
		if (field__help__msg.classList.contains(`slideIn`)) {
			field__help__msg.classList.remove(`slideIn`);
			animateElement({
				element: field__help__msg,
				cssClass: `slideOut`,
				callback: function () {
					field__help__msg.classList.remove(`slideOut`);
					field__help__msg.textContent = '';
				},
				milliseconds: 200,
			});
		}
	};

	registerEventListeners = () => {
		this.fields.forEach((x) => {
			if (!x.isCheckbox) {
				x.input.addEventListener('focus', this.handleFocus);
				x.input.addEventListener('keyup', this.handleKeyup);
				x.input.addEventListener('blur', this.handleBlur);
			} else {
				x.checkbox.addEventListener('change', this.handleCheckbox);
			}
		});
		if (this.submitButton !== null) {
			if (this.className !== `captcha`) {
				this.submitButton.addEventListener('click', this.handleSubmitButton.bind(this));
			}
		}
	};

	handleFocus = (event) => {
		let currentField = this.getCurrentField(event.target);
		if (currentField !== undefined) {
			let classList = currentField.parent.classList;
			classList.add(`field--focused`);
		}
		this.adjustLabels();
	};

	handleKeyup = (event) => {
		let evt = event || window.event;
		let currentField = this.getCurrentField(evt.target);
		if (currentField !== undefined) {
			this.checkIfFieldIsFilled(currentField);
			if (currentField.parent.classList.contains(`field--warning`)) {
				this.adjustErrorLabel(currentField);
			}
		}
	};

	handleBlur = (event) => {
		let evt = event || window.event;
		let currentField = this.getCurrentField(evt.target);
		if (currentField !== undefined) {
			let classList = currentField.parent.classList;
			classList.remove(`field--focused`);
			this.checkIfFieldIsFilled(currentField);
			this.adjustErrorLabel(currentField);
		}
		this.adjustLabels();
	};

	handleCheckbox = (event) => {
		let evt = event || window.event;
		let currentField = this.getCurrentField(evt.target);
		if (currentField !== undefined) {
			this.adjustErrorLabel(currentField);
			this.adjustLabels();
		}
	};

	checkIfFieldIsFilled = (field) => {
		if (!field.isCheckbox) {
			let classList = field.parent.classList;
			if (FormApp.getValueFromInput(field).length > 0) {
				classList.add(`field--notempty`);
			} else {
				classList.remove(`field--notempty`);
			}
		}
	};

	getCurrentField = (field) => {
		return Array.prototype.find.call(this.fields, (x) => x.input === field);
	};

	validateFormOnServer = async (form) => {
		let button = form.submitButton;
		if (!button.classList.contains(`is-loading`)) {
			button.classList.add(`is-loading`);
			let aggregation = form.fields.map((x) => this.validateField(x));
			aggregation = aggregation.reduce((a, v) => a && v.valid);
			let body = form.constructBodyObject();
			body['action'] = 'validate';
			let obj = { body, url: '/validate_form/', csrftoken: this.csrftoken };
			let data = await makeAjaxRequest(obj);
			button.classList.remove(`is-loading`);
			if (!data.hasOwnProperty(`errorMsg`)) {
				if (data.hasOwnProperty(`errors`)) {
					let error_object = {};
					for (let [key, value] of Object.entries(data.errors)) {
						error_object[key] = value[0]['message'];
					}
					let errorKeys = Object.keys(error_object);
					let errorEntries = Object.entries(error_object);
					form.fields.forEach((field) => {
						let index = errorKeys.indexOf(field.name);
						if (index > -1) {
							this.displayErrorInField({
								field: field,
								errorMsg: errorEntries[index][1],
							});
						} else {
							this.removeErrorInField(field);
						}
					});
					if (Object.keys(error_object).length === 0) {
						return {
							data: data,
						};
					} else {
						return { errors: data.errors };
					}
				}
			}
		}
	};

	constructBodyObject = () => {
		let body = this.fields.reduce((a, b) => {
			let val = b.input.value;
			if (b.isCheckbox) {
				val = b.input.checked;
			}
			a[b.name] = val;
			return a;
		}, {});
		body = { form: this.className, ...body };
		return body;
	};
	
	handleSubmitButton = async (event) => {
		let evt = event || window.event;
		evt.preventDefault();
		let res = await this.validateFormOnServer(this);
		if (!res.hasOwnProperty(`errors`)) {
			let data = res.data;
			this.processCaptcha(data);
		}
	};

	processCaptcha = async (data) => {
		let html = data.html;
		let baseForm = this;
		let modal = new Modal({ baseForm, html }); // this.openModal(data.html);
		try {
			let res = await modal.captchaConfirmation();
			await res.modal.closeModal();
			html = res.html;
			let redirectURL = res.redirectURL || `/`;
			let newModal = new Modal({ baseForm, html });
			let res2 = await newModal.messageConfirmation();
			await res2.modal.closeModal(redirectURL);
		} catch (exception) {
			await exception.modal.closeModal();
		}
	};

	static _initForms = (formArray) => {
		formArray.forEach((x, index, my_form) => {
			my_form[index] = new FormApp(x);
			if (!my_form[index].invalid) {
				my_form[index].init();
			}
		});
	};
}
