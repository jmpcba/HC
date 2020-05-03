--'SUMATORIA POR MEDICOS
            SELECT PRAC.ID_PREST, 
						 PREST.CUIT, 
						 PREST.APELLIDO AS "APELLIDO PRESTADOR", 
						 PREST.NOMBRE AS "NOMBRE PRESTADOR", 
						 PREST.SERVICIO, 
						 PREST.ESPECIALIDAD AS ESPECIALIDAD, 
						 PREST.LOCALIDAD AS LOCALIDAD, 
						 ZONAS.NOMBRE AS ZONA, 
						 Sum(PRAC.HS_NORMALES) AS "HS LUN a VIE", 
						 Sum(PRAC.HS_FERIADO) AS "HS SAB DOM y FER", 
						 Sum(PRAC.HS_DIFERENCIAL) AS DIFERENCIAL, 
						 Sum(PRAC.HS_NORMALES+PRAC.HS_FERIADO+PRAC.HS_DIFERENCIAL) AS "TOTAL HORAS", 
						 PREST.MONTO_FIJO AS "MONTO FIJO", 
						 Sum(PRAC.HS_NORMALES*PRAC.MONTO_SEMANA) AS "$ LUN a VIE", IF(PREST.MONTO_FERIADO<>0,Sum(PRAC.HS_FERIADO*PRAC.MONTO_FERIADO),Sum(PRAC.HS_FERIADO*PRAC.MONTO_SEMANA)) AS "$ SAB DOM y FER", Sum(PRAC.HS_DIFERENCIAL*PORCENTAJE) AS "$ DIF", 
						 "$ DIF"+"$ LUN a VIE"+"$ SAB DOM y FER"+"MONTO FIJO" AS "$ TOTAL"
						
						FROM PRESTADORES PREST
						INNER JOIN PRACTICAS PRAC ON PREST.ID = PRAC.ID_PREST
						INNER JOIN ZONAS ON PREST.ZONA = ZONAS.ID
						
						WHERE PRAC.FECHA_PRACTICA Between #{0}# And #{1}#
						
						GROUP BY PRAC.ID_PREST, PREST.CUIT, PREST.APELLIDO, PREST.NOMBRE, PREST.SERVICIO, PREST.ESPECIALIDAD, PREST.LOCALIDAD, ZONAS.NOMBRE, PREST.MONTO_FIJO, PREST.MONTO_SEMANA, PREST.MONTO_FERIADO;

        ElseIf _liq = tiposLiquidacion.paciente Then

            'SUMATORIA POR PACIENTE
            'USAR QUERY_SUMATORIA_PACIENTE EN ACCESS PARA GENERAR SQL
            cmd.CommandText = String.Format("Select PACIENTES.AFILIADO, PACIENTES.APELLIDO As [APELLIDO PACIENTE], PACIENTES.NOMBRE As [NOMBRE PACIENTE], Sum(PRAC.HS_NORMALES) As [HS LUN a VIE], Sum(PRAC.HS_FERIADO) As [HS SAB DOM y FER], Sum(PRAC.HS_DIFERENCIAL) AS DIFERENCIAL
                                From PACIENTES INNER JOIN (PREST INNER JOIN PRAC ON PREST.ID = PRAC.ID_PREST) ON PACIENTES.AFILIADO = PRAC.AFILIADO
                                WHERE (((PRAC.FECHA_PRACTICA) Between #{0}# And #{1}#))
                                GROUP BY PACIENTES.AFILIADO, PACIENTES.APELLIDO, PACIENTES.NOMBRE", desde.ToShortDateString, hasta.ToShortDateString)

            'LIQUIDACIONES CERRADAS
        ElseIf _liq = tiposLiquidacion.cerrada Then

            cmd.CommandText = String.Format("SELECT LIQUIDACION.ID, LIQUIDACION.ID_PREST, LIQUIDACION.CUIT, PREST.APELLIDO AS [APELLIDO PRESTADOR], PREST.NOMBRE, LIQUIDACION.LOCALIDAD, LIQUIDACION.ESPECIALIDAD, LIQUIDACION.HS_NORMALES AS [HS LUN a VIE], LIQUIDACION.HS_FERIADOS AS [HS SAB DOM Y FER], LIQUIDACION.HS_DIFERENCIAL AS DIFERENCIAL, [HS_NORMALES]+[HS_FERIADOS]+[HS_DIFERENCIAL] AS [TOTAL HORAS], LIQUIDACION.MONTO_FIJO AS [MONTO FIJO], LIQUIDACION.IMPORTE_NORMAL AS [$ LUN a VIE], LIQUIDACION.IMPORTE_FERIADO AS [$ SAB DOM y FER], LIQUIDACION.IMPORTE_DIFERENCIAL AS [$ DIF], [$ DIF]+[$ LUN a VIE]+[$ SAB DOM y FER]+[MONTO FIJO] AS [$ TOTAL]
                                FROM LIQUIDACION INNER JOIN PREST ON LIQUIDACION.ID_PREST = PREST.ID
                                WHERE (((LIQUIDACION.MES)=#{0}#))", hasta.ToShortDateString)
