$(document).ready(function() {
    $("#benh_nhan_search").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api/search_benh_nhan",
                dataType: "json",
                data: {
                    q: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item.name,
                            value: item.name,
                            id: item.id
                        };
                    }));
                }
            });
        },
        minLength: 2,
        select: function(event, ui) {
            $("#benh_nhan_id").val(ui.item.id);
        }
    });

    let thuocCounter = 0;
    $("#add-thuoc").click(function() {
        const thuocHtml = `
            <div class="thuoc-item">
                <select name="thuoc_list-${thuocCounter}-thuoc_id" class="form-control">
                    {% for thuoc in Thuoc.query.all() %}
                    <option value="{{ thuoc.id }}">{{ thuoc.ten_thuoc }}</option>
                    {% endfor %}
                </select>
                <input type="number" name="thuoc_list-${thuocCounter}-so_luong" class="form-control" required>
                <button type="button" class="btn btn-danger remove-thuoc">Xóa</button>
            </div>
        `;
        $("#thuoc-container").append(thuocHtml);
        thuocCounter++;
    });

    $(document).on("click", ".remove-thuoc", function() {
        $(this).closest(".thuoc-item").remove();
    });
});
