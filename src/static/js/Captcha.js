import { makeAjaxRequest } from './ajax.js';
export default class Captcha {
	constructor(modal) {
		this.modal = modal;
		this.captchaImage = null;
		this.captchaForm = null;
	}

	update = async () => {
		let image = await this.getCaptchaImage();
		this.captchaImage = image;
	};

	getCaptchaImage = async () => {
		let image = new Image();
		image.style.height = '41px';
		image.style.width = 'auto';
		let data = await makeAjaxRequest({
			url: `/get_captcha_image/`,
			body: ``,
			csrftoken: this.modal.baseForm.csrftoken,
		});
		if (!data.hasOwnProperty(`errorMsg`)) {
			let b64str = data.img.replace(/['"]+/g, '');
			image.src = 'data:image/png;base64,' + b64str;
		}
		return image;
	};
}
