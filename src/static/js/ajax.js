export function makeAjaxRequest({ url, body, csrftoken }) {
	return fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
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
