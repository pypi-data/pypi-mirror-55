#ifndef _PROTON_SRC_REACTOR_H
#define _PROTON_SRC_REACTOR_H 1

/*
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 */

#include <proton/reactor.h>
#include <proton/url.h>

void pni_record_init_reactor(pn_record_t *record, pn_reactor_t *reactor);
void pni_reactor_set_connection_peer_address(pn_connection_t *connection,
                                             const char *host,
                                             const char *port);
pn_io_t *pni_reactor_io(pn_reactor_t *reactor);

#endif /* src/reactor.h */
