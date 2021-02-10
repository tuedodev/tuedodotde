export function makeAjaxRequest({ url, body, csrftoken, lang='de' }) {
	return fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
			'Accept-Language': lang
		},
		body: JSON.stringify(body),
	})
		.then((res) => res.json())
		.then((data) => {
			return data;
		})
		.catch((e) => {
			return { errorMsg: 'Ein Fehler ist aufgetreten.' };
		});
}
