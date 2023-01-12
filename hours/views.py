import io
from django.http import HttpResponseRedirect, HttpResponse
from io import BytesIO
from django.shortcuts import render
import pandas as pd
import numpy as np
from datetime import datetime
from hours.forms import CalculateForm


def handle_uploaded_file(file_handle):
    df = pd.read_csv(
        io.StringIO(file_handle.decode("utf-8")),
        sep=";",
        usecols=["usuario", "data_evento"],
        parse_dates=["data_evento"],
    )

    df["data_evento"] = df["data_evento"].astype(str)
    df["dia"] = df["data_evento"].str[:10]
    df["horario"] = df["data_evento"].str[11:19]

    df["dia"] = pd.to_datetime(df["dia"], infer_datetime_format=True)
    df["horario"] = pd.to_datetime(df["horario"], infer_datetime_format=True)

    df = df.loc[df["usuario"] != "Usuario Desconhecido"]

    df = df.sort_values(["usuario", "dia"])

    df_full = df.groupby(["usuario", "dia"])["horario"]

    zero = pd.to_timedelta("00:00:00")
    tres = pd.to_timedelta("03:00:00")
    dezoitoetrinta = pd.to_timedelta("18:30:00")
    doismin = pd.to_timedelta("00:02:00")
    doish = pd.to_timedelta("02:00:00")
    cinco = pd.to_timedelta("05:00:00")

    oito = pd.to_datetime("08:00:00", infer_datetime_format=True)
    nove = pd.to_datetime("09:00:00", infer_datetime_format=True)
    dezemeia = pd.to_datetime("10:30:00", infer_datetime_format=True)
    doze = pd.to_datetime("12:00:00", infer_datetime_format=True)
    dozetrinta = pd.to_datetime("12:30:00", infer_datetime_format=True)
    treze = pd.to_datetime("13:00:00", infer_datetime_format=True)
    catorze = pd.to_datetime("14:00:00", infer_datetime_format=True)
    quinze = pd.to_datetime("15:00:00", infer_datetime_format=True)
    dezeseis = pd.to_datetime("16:00:00", infer_datetime_format=True)
    dezesete = pd.to_datetime("17:00:00", infer_datetime_format=True)
    dezoito = pd.to_datetime("18:00:00", infer_datetime_format=True)
    dezoitoquinze = pd.to_datetime("18:15:00", infer_datetime_format=True)
    dezoitotrinta = pd.to_datetime("18:30:00", infer_datetime_format=True)
    vinte = pd.to_datetime("20:00:00", infer_datetime_format=True)
    vinteum = pd.to_datetime("21:00:00", infer_datetime_format=True)
    vintedois = pd.to_datetime("22:00:00", infer_datetime_format=True)

    list_df = []

    for key, group in df_full:
        if group.count() == 1:
            if all(group < nove):
                list_df.append(
                    (key[0], key[1], (group.min() + tres) - group.min(), "Matutino")
                )
            elif all(group > nove) & all(group < dezemeia):
                list_df.append((key[0], key[1], doze - group.min(), "Matutino"))
            elif all(group > dezemeia) & all(group < treze):
                list_df.append(
                    (key[0], key[1], group.min() - (group.min() - tres), "Matutino")
                )
            elif all(group > treze) & all(group < quinze):
                list_df.append(
                    (key[0], key[1], (group.min() + tres) - group.min(), "Vespertino")
                )
            elif all(group > quinze) & all(group < dezeseis):
                list_df.append((key[0], key[1], dezoito - group.min(), "Vespertino"))
            elif all(group > dezeseis) & all(group < dezoitoquinze):
                list_df.append(
                    (key[0], key[1], group.min() - (group.min() - tres), "Vespertino")
                )
            elif all(group > dezoitoquinze) & all(group < vinte):
                list_df.append(
                    (key[0], key[1], (group.min() + tres) - group.min(), "Noturno")
                )
            elif all(group > vinte) & all(group < vinteum):
                list_df.append(
                    (key[0], key[1], (group.min() - dezoitoetrinta), "Noturno")
                )
            elif all(group > vinteum):
                list_df.append(
                    (key[0], key[1], group.min() - (group.min() - tres), "Noturno")
                )

        if group.count() == 2:
            if all(group < dozetrinta):
                list_df.append((key[0], key[1], group.max() - group.min(), "Matutino"))
            elif all(group > dozetrinta) & all(group < dezoitotrinta):
                list_df.append(
                    (key[0], key[1], group.max() - group.min(), "Vespertino")
                )
            elif all(group > dezoitotrinta):
                list_df.append((key[0], key[1], group.max() - group.min(), "Noturno"))

        if group.count() == 3:
            if bool(group.max() < dozetrinta):
                list_df.append((key[0], key[1], group.max() - group.min(), "Matutino"))
            elif bool(group.max() > dozetrinta) & bool(group.max() < dezoitotrinta):
                list_df.append(
                    (key[0], key[1], group.max() - group.min(), "Vespertino")
                )
            elif bool(group.max() > dezoitotrinta):
                list_df.append((key[0], key[1], group.max() - group.min(), "Noturno"))

        val_4 = []
        if group.count() == 4:
            if bool(group.max() < dozetrinta):
                list_df.append((key[0], key[1], group.max() - group.min(), "Matutino"))
            elif bool(group.max() > dozetrinta) & bool(group.max() < dezoitotrinta):
                for i in group:
                    val_4.append(i)
                if ((val_4[0] - val_4[1]) < doismin) and (
                    (val_4[2] - val_4[3]) < doismin
                ):
                    list_df.append(
                        (key[0], key[1], (val_4[0] - val_4[3]), "Vespertino")
                    )
                else:
                    list_df.append(
                        (
                            key[0],
                            key[1],
                            (val_4[0] - val_4[1]) + (val_4[2] - val_4[3]),
                            "Vespertino",
                        )
                    )
            elif bool(group.max() > dezoitotrinta):
                for i in group:
                    val_4.append(i)
                if ((val_4[0] - val_4[1]) < doismin) and (
                    (val_4[2] - val_4[3]) < doismin
                ):
                    list_df.append((key[0], key[1], (val_4[0] - val_4[3]), "Noturno"))
                else:
                    list_df.append(
                        (
                            key[0],
                            key[1],
                            (val_4[0] - val_4[1]) + (val_4[2] - val_4[3]),
                            "Noturno",
                        )
                    )

        val_5 = []
        if group.count() > 5:
            if bool(group.max() > oito):
                for g in group:
                    val_5.append(g)
                t = len(val_5) - 1
                for i in range(0, len(val_5)):
                    if t == 0:
                        break
                    if not (val_5[i] - (val_5[len(val_5) - t])) > doismin:
                        t -= 1
                        pass
                    elif not (val_5[i] - (val_5[len(val_5) - t])) > doish:
                        t -= 1
                        pass
                    elif (val_5[i] - (val_5[len(val_5) - t])) > cinco:
                        t -= 1
                        pass
                    else:
                        if val_5[i] < dozetrinta:
                            list_df.append(
                                (
                                    key[0],
                                    key[1],
                                    val_5[i] - (val_5[len(val_5) - t]),
                                    "Matutino",
                                )
                            )
                            t -= 1
                        elif (val_5[i] > dozetrinta) & (val_5[i] < dezoitotrinta):
                            list_df.append(
                                (
                                    key[0],
                                    key[1],
                                    val_5[i] - (val_5[len(val_5) - t]),
                                    "Vespertino",
                                )
                            )
                            t -= 1
                        elif val_5[i] > dezoitotrinta:
                            list_df.append(
                                (
                                    key[0],
                                    key[1],
                                    val_5[i] - (val_5[len(val_5) - t]),
                                    "Noturno",
                                )
                            )
                            t -= 1

    df_clean = pd.DataFrame(list_df, columns=["usuario", "dia", "hora", "turno"])
    df_clean = df_clean.sort_values(["usuario", "dia"])
    df_done = df_clean.groupby(["usuario"])["hora"]

    # display(df_clean.head(15))

    list_done = []
    h = zero
    for k, v in df_done:
        for i in v:
            h = h + i
        list_done.append((k, h))
        h = zero

    df_done_2 = pd.DataFrame(list_done, columns=["usuario", "total_hora"])

    # with pd.ExcelWriter(f"arquivo-{datetime.now().date()}.xlsx") as writer:
    #     df_clean.to_excel(writer, sheet_name="Horas_diarias")
    #     df_done_2.to_excel(writer, sheet_name="Horas_total")

    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine="xlsxwriter")
        df_clean.to_excel(writer, sheet_name="Horas_diarias")
        df_done_2.to_excel(writer, sheet_name="Horas_total")
        writer.save()
        # Set up the Http response.
        filename = f"arquivo-{datetime.now().date()}.xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=%s" % filename
        return response

    # writer = pd.ExcelWriter(
    #     f"arquivo-{datetime.now().date()}.xlsx", engine="xlsxwriter"
    # )

    # df_clean.to_excel(writer, sheet_name="Horas_diarias")
    # df_done_2.to_excel(writer, sheet_name="Horas_total")

    # writer.close()

    # return writer

    # df_done_2.to_excel(f'arquivo-{datetime.now().date()}.xls')
    # df_done_2.head(50)
    # df_done_2.info()


def index(request):

    if request.method == "POST":
        form = CalculateForm(request.POST, request.FILES)
        if form.is_valid():

            handle = handle_uploaded_file(request.FILES["up_file"].read())

            return handle
    else:
        form = CalculateForm()

    return render(
        request,
        "index.html",
        {
            "form": form,
        },
    )
